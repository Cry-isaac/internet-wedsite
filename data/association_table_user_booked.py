from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

association_table_user = Table(
    'student_course', Base.metadata,
    Column('student_id', ForeignKey('students.id')),
    Column('course_id', ForeignKey('courses.id'))
)