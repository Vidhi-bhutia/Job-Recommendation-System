from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from dotenv import load_dotenv
from src.helper import extract_text_from_pdf, ask_gemini, match_resume_to_job
from src.job_api import (
	fetch_linkedin_jobs,
	fetch_workday_jobs,
)


load_dotenv(override=True)
app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB uploads

JOB_SOURCES = {
	"linkedin": fetch_linkedin_jobs,
	"workday": fetch_workday_jobs,
}


def _normalize_job(job):
	"""Normalize job dictionaries from different providers."""
	return {
		"title": job.get("title")
		or job.get("jobTitle")
		or job.get("position")
		or "Untitled role",
		"company": job.get("companyName")
		or job.get("company")
		or job.get("employer")
		or "Company N/A",
		"location": job.get("location") or job.get("city") or "Location N/A",
		"url": job.get("url")
		or job.get("jobUrl")
		or job.get("applyUrl")
		or job.get("canonicalUrl"),
		"snippet": job.get("description")
		or job.get("descriptionSnippet")
		or job.get("summary")
		or job.get("text")
		or "",
		"source": job.get("source") or job.get("jobSource") or "",
	}


def _summarize_resume(text: str) -> str:
	prompt = (
		"Extract the top 5 skills and 3 role keywords from this resume. "
		"Return bullet points only.\n\n" + text
	)
	return ask_gemini(prompt)


@app.route("/", methods=["GET"])
def index():
	return render_template("home.html")


@app.route("/details", methods=["GET"])
def details():
	return render_template("details.html", query="", location="India", rows=5)


@app.route("/search", methods=["POST"])
def search():
	query = request.form.get("query", "").strip()
	location = request.form.get("location", "India").strip() or "India"
	rows = 5
	try:
		rows = int(request.form.get("rows", 5))
		rows = min(max(rows, 1), 20)
	except (ValueError, TypeError):
		rows = 5
	
	selected_sources = request.form.getlist("sources") or list(JOB_SOURCES.keys())

	if not query:
		flash("Please enter a target role to search for jobs.")
		return redirect(url_for("details"))

	resume_file = request.files.get("resume")
	resume_summary = None
	resume_text = ""
	errors = []

	if resume_file and resume_file.filename:
		if not resume_file.filename.lower().endswith(".pdf"):
			flash("Only PDF resumes are supported.")
			return redirect(url_for("details"))
		try:
			resume_text = extract_text_from_pdf(resume_file)
			if resume_text.strip():
				try:
					resume_summary = _summarize_resume(resume_text)
				except Exception as exc:  # noqa: BLE001
					errors.append(f"Resume summary failed: {exc}")
		except Exception as exc:
			errors.append(f"PDF extraction failed: {exc}")

	jobs = []
	for source in selected_sources:
		fetcher = JOB_SOURCES.get(source)
		if not fetcher:
			continue
		try:
			raw_jobs = fetcher(query, location=location, rows=rows)
			if raw_jobs:
				normalized = [_normalize_job(job) for job in raw_jobs]
				for job in normalized:
					job["source"] = job.get("source") or source.capitalize()
				jobs.extend(normalized)
		except Exception as exc:  # noqa: BLE001
			errors.append(f"{source.title()} search failed: {str(exc)}")

	# Resume Matching
	if resume_text.strip() and jobs:
		for i, job in enumerate(jobs[:15]):
			try:
				match_data = match_resume_to_job(resume_text, job['title'], job['snippet'])
				job['match_score'] = match_data.get('percentage', 0)
				job['match_tips'] = match_data.get('tips', [])
			except Exception as e:
				print(f"Matching failed for job {i}: {e}")

	return render_template(
		"results.html",
		jobs=jobs if jobs else None,
		resume_summary=resume_summary,
		query=query,
		location=location,
	)




if __name__ == "__main__":
	print("Starting TalentFlow AI...")
	print("Open http://localhost:5000 in your browser")
	app.run(debug=True, host="0.0.0.0", port=5000)
