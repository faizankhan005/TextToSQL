import sqlite3


## connect to the sqlite database
connection = sqlite3.connect('student.db')


## create a cursor object to insert record, create tables, retrieve into the database
cursor = connection.cursor()

## create a table
table_info="""create table 
            STUDENT(NAME VARCHAR(25),
            CLASS VARCHAR(25), 
            AGE INTEGER, 
            GENDER VARCHAR(10), 
            ADDRESS VARCHAR(50), 
            SECTION VARCHAR(10),
            MARKS INTEGER);"""

cursor.execute(table_info)

## insert some more records into the table

cursor.execute("INSERT INTO STUDENT VALUES('John Doe', '10th Grade', 15, 'Male', '123 Main St', 'A', 85)")
cursor.execute("INSERT INTO STUDENT VALUES('Jane Smith', '11th Grade', 16, 'Female', '456 Oak Ave', 'B', 90)")
cursor.execute("INSERT INTO STUDENT VALUES('Michael Johnson', '12th Grade', 17, 'Male', '789 Pine Rd', 'A', 78)")
cursor.execute("INSERT INTO STUDENT VALUES('Emily Davis', '10th Grade', 15, 'Female', '101 Maple St', 'A', 92)")
cursor.execute("INSERT INTO STUDENT VALUES('William Brown', '11th Grade', 16, 'Male', '202 Cedar Ave', 'C', 68)")
cursor.execute("INSERT INTO STUDENT VALUES('Olivia Wilson', '12th Grade', 17, 'Female', '303 Birch Rd', 'B', 88)")
cursor.execute("INSERT INTO STUDENT VALUES('James Miller', '10th Grade', 15, 'Male', '404 Elm St', 'A', 95)")
cursor.execute("INSERT INTO STUDENT VALUES('Sophia Moore', '11th Grade', 16, 'Female', '505 Walnut Ave', 'A', 91)")
cursor.execute("INSERT INTO STUDENT VALUES('Benjamin Taylor', '12th Grade', 17, 'Male', '606 Ash Rd', 'B', 82)")
cursor.execute("INSERT INTO STUDENT VALUES('Isabella Anderson', '10th Grade', 15, 'Female', '707 Cherry St', 'A', 89)")
cursor.execute("INSERT INTO STUDENT VALUES('Lucas Thomas', '11th Grade', 16, 'Male', '808 Spruce Ave', 'C', 71)")
cursor.execute("INSERT INTO STUDENT VALUES('Mia Jackson', '12th Grade', 17, 'Female', '909 Willow Rd', 'B', 86)")
cursor.execute("INSERT INTO STUDENT VALUES('Ethan White', '10th Grade', 15, 'Male', '111 Lake St', 'A', 94)")
cursor.execute("INSERT INTO STUDENT VALUES('Charlotte Harris', '11th Grade', 16, 'Female', '222 River Ave', 'A', 97)")
cursor.execute("INSERT INTO STUDENT VALUES('Alexander Martin', '12th Grade', 17, 'Male', '333 Hill Rd', 'B', 80)")
cursor.execute("INSERT INTO STUDENT VALUES('Amelia Thompson', '10th Grade', 15, 'Female', '444 Valley St', 'A', 93)")
cursor.execute("INSERT INTO STUDENT VALUES('Daniel Garcia', '11th Grade', 16, 'Male', '555 Forest Ave', 'C', 65)")
cursor.execute("INSERT INTO STUDENT VALUES('Harper Martinez', '12th Grade', 17, 'Female', '666 Sunset Rd', 'B', 84)")
cursor.execute("INSERT INTO STUDENT VALUES('Matthew Robinson', '10th Grade', 15, 'Male', '777 Sunrise St', 'A', 87)")
cursor.execute("INSERT INTO STUDENT VALUES('Evelyn Clark', '11th Grade', 16, 'Female', '888 Garden Ave', 'A', 96)")



## display all records from the table
print("the inserted records are:")

data = cursor.execute("SELECT * FROM STUDENT")

for row in data:
    print(row)


## close the connection to the database
connection.commit()
connection.close()