print("=================================")
print("   STUDENT SKILL GAP ANALYZER")
print("=================================")

name = input("Enter your name: ")

print("\nChoose your target career")
print("1. Python Developer")
print("2. Data Analyst")
print("3. Web Developer")

choice = int(input("Enter your choice: "))

print("\nRate your skills from 1 to 5")
print("1 = Beginner")
print("5 = Excellent")

python = int(input("Python: "))
sql = int(input("SQL: "))
dsa = int(input("DSA: "))
oops = int(input("OOP: "))
# Career requirements

if choice == 1:
    career = "Python Developer"

    required_python = 5
    required_sql = 4
    required_dsa = 4
    required_oops = 4

elif choice == 2:
    career = "Data Analyst"

    required_python = 4
    required_sql = 5
    required_dsa = 2
    required_oops = 2

elif choice == 3:
    career = "Web Developer"

    required_python = 3
    required_sql = 3
    required_dsa = 3
    required_oops = 3

else:
    print("Invalid choice")
    exit()

    print("\n=================================")
print("        YOUR SKILL GAP")
print("=================================")

print("Target Career:", career)

print("\nPython:")
print("Your level:", python)
print("Required:", required_python)

print("\nSQL:")
print("Your level:", sql)
print("Required:", required_sql)

print("\nDSA:")
print("Your level:", dsa)
print("Required:", required_dsa)

print("\nOOP:")
print("Your level:", oops)
print("Required:", required_oops)

python_gap = required_python - python
sql_gap = required_sql - sql
dsa_gap = required_dsa - dsa
oops_gap = required_oops - oops

print("\n=================================")
print("       GAP CALCULATION")
print("=================================")

print("Python gap:", max(0, python_gap))
print("SQL gap:", max(0, sql_gap))
print("DSA gap:", max(0, dsa_gap))
print("OOP gap:", max(0, oops_gap))

print("\n=================================")
print("       IMPROVEMENT PRIORITY")
print("=================================")

if dsa_gap >= 3:
    print("DSA: HIGH PRIORITY 🔴")
elif dsa_gap > 0:
    print("DSA: NEEDS IMPROVEMENT 🟠")
else:
    print("DSA: GOOD ✓")

if sql_gap >= 3:
    print("SQL: HIGH PRIORITY 🔴")
elif sql_gap > 0:
    print("SQL: NEEDS IMPROVEMENT 🟠")
else:
    print("SQL: GOOD ✓")

if oops_gap >= 3:
    print("OOP: HIGH PRIORITY 🔴")
elif oops_gap > 0:
    print("OOP: NEEDS IMPROVEMENT 🟠")
else:
    print("OOP: GOOD ✓")

if python_gap >= 3:
    print("Python: HIGH PRIORITY 🔴")
elif python_gap > 0:
    print("Python: NEEDS IMPROVEMENT 🟠")
else:
    print("Python: GOOD ✓")
total_student_score = python + sql + dsa + oops
total_required_score = required_python + required_sql + required_dsa + required_oops

readiness = (total_student_score / total_required_score) * 100

print("\n=================================")
print("       CAREER READINESS")
print("=================================")

print("Target Career:", career)
print("Your Readiness:", round(readiness, 2), "%")
print("\nRecommendation:")

if readiness >= 80:
    print("Excellent! You are well prepared for this career.")
elif readiness >= 60:
    print("Good progress. Improve your skill gaps before applying.")
elif readiness >= 40:
    print("You need more preparation. Focus on your high-priority skills.")
else:
    print("You need significant improvement. Start with the recommended skills.")
print("\n=================================")
print("     PERSONALIZED ROADMAP")
print("=================================")

if dsa_gap > 0:
    print("\nDSA:")
    print("→ Learn Arrays")
    print("→ Learn Strings")
    print("→ Learn Searching")
    print("→ Learn Sorting")

if sql_gap > 0:
    print("\nSQL:")
    print("→ Learn SELECT")
    print("→ Learn WHERE")
    print("→ Learn JOIN")
    print("→ Learn GROUP BY")

if oops_gap > 0:
    print("\nOOP:")
    print("→ Learn Classes and Objects")
    print("→ Learn Inheritance")
    print("→ Learn Polymorphism")

if python_gap > 0:
    print("\nPython:")
    print("→ Improve Python basics")
    print("→ Practice Functions")
    print("→ Learn File Handling")