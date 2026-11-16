"""Create the DB and synthetic DEMO accounts. These are NOT real VIPS personnel."""
from datetime import datetime, timedelta
from core.database import init_db, get_conn
from core.auth import hash_password

DEMO_PW = "Demo@1234"

def seed():
    init_db()
    with get_conn() as c:
        if c.execute("SELECT 1 FROM users LIMIT 1").fetchone():
            print("Database already seeded."); return
        def add(name, email, role, approved=1):
            return c.execute("INSERT INTO users(full_name,email,password_hash,role,is_approved,is_demo) "
                             "VALUES(?,?,?,?,?,1)", (name, email, hash_password(DEMO_PW), role, approved)).lastrowid
        add("Demo Admin", "admin.demo@vips.edu", "admin")
        s = add("Demo Student", "student.demo@vips.edu", "student")
        c.execute("INSERT INTO student_profiles VALUES(?,?,?,?)", (s, "BCA", 3, 5))
        c.execute("INSERT INTO notification_prefs(student_id) VALUES(?)", (s,))
        providers = [
            ("Demo Counsellor", "counsellor.demo@vips.edu", "counsellor", "College Counsellor",
             "Demo Counsellor (sample)", "Academic stress, anxiety, adjustment", "Sample profile for demonstration."),
            ("Demo Faculty Mentor", "faculty.demo@vips.edu", "mentor", "Faculty Mentor",
             "Demo Faculty (sample)", "Career guidance, study planning", "Sample profile for demonstration."),
            ("Demo Peer Mentor", "peer.demo@vips.edu", "mentor", "Trained Peer Mentor",
             "Demo Peer Mentor (sample)", "Friendships, settling in", "Sample profile. Peer mentors are not professionals."),
        ]
        for name, email, role, ptype, desig, exp, intro in providers:
            pid = add(name, email, role)
            c.execute("INSERT INTO provider_profiles VALUES(?,?,?,?,?)", (pid, ptype, desig, exp, intro))
            for d in (1, 2, 3):   # sample slots, clearly demo data
                t = (datetime.now() + timedelta(days=d)).replace(hour=11, minute=0, second=0, microsecond=0)
                c.execute("INSERT INTO availability_slots(provider_id,slot_start) VALUES(?,?)", (pid, t.isoformat()))
    print("Seeded demo accounts (password for all: %s)" % DEMO_PW)

if __name__ == "__main__":
    seed()
