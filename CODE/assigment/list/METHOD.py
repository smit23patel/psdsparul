# CREATE (List acts like a folder)
student = ["Smit", 20040927]
print("Student list created:", student)

# READ
print("Name:", student[0])
print("DOB:", student[1])

# UPDATE
student[0] = "Smit Patel"
student[1] = 20030927
print("Updated student list:", student)

# APPEND
student.append("Python Course")
print("After append:", student)

# INSERT
student.insert(1, "IT")
print("After insert:", student)

# COPY
student_copy = student.copy()
print("Copied list:", student_copy)

# REMOVE
student.remove(20030927)
print("After removing DOB:", student)

# POP
student.pop()
print("After pop:", student)

# CLEAR
student.clear()
print("After clear:", student)
