from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STR']

engine = create_engine(
  db_connection_string,
  connect_args={
    "ssl": {
      "ca": "ca_cert/isrgrootx1.pem",
    }
})

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for row in result.all():
      jobs.append(row._asdict())
    return jobs

def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text(f"select * from jobs where id = {id}"))
    rows = []
    for row in result.all():
      rows.append(row._asdict())
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0])

def add_application_to_db(job_id, data):
  query_string = "INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) " \
   + "VALUES (" + str(job_id) + ", '" + data['full_name'] + "', '" + data['email'] + "', '" \
   + data['linkedin_url'] + "', '" + data['education'] + "', '" + data['work_experience'] + "', '" \
   + data['resume_url'] + "')"
  
  with engine.connect() as conn:
    query = text(query_string)
    conn.execute(query)
    conn.commit()