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

# DELETE
student.remove(20030927)
print("After deleting DOB:", student)
