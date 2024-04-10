import json

def student_average(stud_code, dbsize):
    # open the file
    with open(dbsize + '_exams.json', 'r', encoding='utf8') as f:
        exams = json.load(f)
    # filter the exams of the student
    exams = [e for e in exams if e['stud_code'] == stud_code]
    # compute the average
    if len(exams) == 0:
        return 0
    else:
        return round(sum(e['grade'] for e in exams) / len(exams), 2)
    pass

def course_average(course_code, dbsize):
    # open the file
    with open(dbsize + '_exams.json', 'r', encoding='utf8') as f:
        exams = json.load(f)
    # filter the exams of the course
    exams = [e for e in exams if e['course_code'] == course_code]
# compute the average
    if len(exams) == 0:
        return 0
    else:
        return round(sum(e['grade'] for e in exams) / len(exams), 2)


    pass

def teacher_average(teach_code, dbsize):
    # Load exams data
    with open(dbsize + '_exams.json', 'r', encoding='utf8') as f:
        exams = json.load(f)
    # Load courses data
    with open(dbsize + '_courses.json', 'r', encoding='utf8') as f:
        courses = json.load(f)

    # Filter courses taught by the teacher
    teacher_courses = [course['course_code'] for course in courses if course['teach_code'] == teach_code]
    # Filter exams for these courses
    teacher_exams = [exam for exam in exams if exam['course_code'] in teacher_courses]

    # Compute the average
    if len(teacher_exams) == 0:
        return 0
    else:
        return round(sum(e['grade'] for e in teacher_exams) / len(teacher_exams), 2)


def top_students(dbsize):
    # Load students data
    with open(dbsize + '_students.json', 'r', encoding='utf8') as f:
        students = json.load(f)
    # Load exams data
    with open(dbsize + '_exams.json', 'r', encoding='utf8') as f:
        exams = json.load(f)

    student_averages = {}
    for student in students:
        student_exams = [e for e in exams if e['stud_code'] == student['stud_code']]
        if student_exams:
            average = round(sum(e['grade'] for e in student_exams) / len(student_exams), 2)
            if average >= 28:
                # Include both the average and the student's full name for sorting
                student_averages[student['stud_code']] = (average, f"{student['stud_surname']} {student['stud_name']}")

    # Sort by average grade in descending order and then by name in case of a tie
    sorted_students = sorted_students = sorted(student_averages.items(), key=lambda x: (-x[1][0], x[1][1], x[0]))

    return [code for code, _ in sorted_students]


def print_recorded_exams(stud_code, dbsize, fileout):
    # Load the necessary data
    with open(dbsize + '_students.json', 'r', encoding='utf8') as f:
        students = json.load(f)
    with open(dbsize + '_exams.json', 'r', encoding='utf8') as f:
        exams = json.load(f)
    with open(dbsize + '_courses.json', 'r', encoding='utf8') as f:
        courses = json.load(f)

    # Find the student
    student = next((s for s in students if s['stud_code'] == stud_code), None)
    if not student:
        return  # Student not found

    # Filter exams taken by the student and sort
    student_exams = [exam for exam in exams if exam['stud_code'] == stud_code]
    student_exams.sort(key=lambda x: (x['date'], next(c['course_name'] for c in courses if c['course_code'] == x['course_code'])))

    # Determine the maximum length of course names for formatting
    max_course_name_length = max(len(next(c['course_name'] for c in courses if c['course_code'] == exam['course_code'])) for exam in student_exams)

    # Write to the file
    with open(fileout, 'w', encoding='utf8') as f:
        # Header
        f.write(
            f"Exams taken by student {student['stud_surname']} {student['stud_name']}, student number {stud_code}\n")

        # Exam details
        for exam in student_exams:
            course_name = next(c['course_name'] for c in courses if c['course_code'] == exam['course_code'])
            padding = ' ' * (max_course_name_length - len(course_name))  # Calculate padding for each line
            formatted_line = f"{course_name}{padding}\t{exam['date']}\t{exam['grade']}\n"
            f.write(formatted_line)

    # Return the number of exams taken by the student
    return len(student_exams)


def print_top_students(dbsize, fileout):
    # Load data and compute top students
    with open(dbsize + '_students.json', 'r', encoding='utf8') as f:
        students = json.load(f)
    with open(dbsize + '_exams.json', 'r', encoding='utf8') as f:
        exams = json.load(f)

    student_averages = {}
    for student in students:
        student_exams = [e for e in exams if e['stud_code'] == student['stud_code']]
        if student_exams:
            average = round(sum(e['grade'] for e in student_exams) / len(student_exams), 2)
            if average >= 28:
                student_averages[student['stud_code']] = (average, f"{student['stud_surname']} {student['stud_name']}")

    # Determine the maximum length of the names for formatting
    max_name_length = max(len(student[1]) for student in student_averages.values())

    sorted_students = sorted(student_averages.items(), key=lambda x: (-x[1][0], x[1][1], x[0]))

    # Formatting and writing to file
    with open(fileout, 'w', encoding='utf8') as f:
        for stud_code, (average, name) in sorted_students:
            f.write(f"{name:<{max_name_length}}\t{average}\n")

    # Return the number of rows saved
    return len(sorted_students)


def print_exam_record(exam_code, dbsize, fileout):
    # open the file
    with open(dbsize + '_exams.json', 'r', encoding='utf8') as f:
        exams = json.load(f)
    # filter the exam
    exams = [e for e in exams if e['exam_code'] == exam_code]
    # open the output file
    with open(fileout, 'w', encoding='utf8') as file:
        #get the exam code, course code, date, grade, and student code
        exam_code = exams[0]['exam_code']
        course_code = exams[0]['course_code']
        date = exams[0]['date']
        grade = exams[0]['grade']
        stud_code = exams[0]['stud_code']
        #get the student name and surname from the student code
        with open(dbsize + '_students.json', 'r', encoding='utf8') as f:
            students = json.load(f)
        students = [s for s in students if s['stud_code'] == stud_code]
        stud_name = students[0]['stud_name']
        stud_surname = students[0]['stud_surname']
        #get the course name from the course code and the teacher code
        with open(dbsize + '_courses.json', 'r', encoding='utf8') as f:
            courses = json.load(f)
        courses = [c for c in courses if c['course_code'] == course_code]
        course_name = courses[0]['course_name']
        teach_code = courses[0]['teach_code']
        #get the teacher name and surname from the teacher code
        with open(dbsize + '_teachers.json', 'r', encoding='utf8') as f:
            teachers = json.load(f)
        teachers = [t for t in teachers if t['teach_code'] == teach_code]
        teach_name = teachers[0]['teach_name']
        teach_surname = teachers[0]['teach_surname']
        #write the exam record

        file.write('The student {} {}, student number {}, took on {} the {} exam with the teacher {} {} with grade {}.'.format( stud_name,stud_surname, stud_code, date, course_name, teach_name, teach_surname, grade))

    # return the grade
    return grade
    pass

if __name__ == '__main__':
    print_top_students('large', 'top_students.txt')

