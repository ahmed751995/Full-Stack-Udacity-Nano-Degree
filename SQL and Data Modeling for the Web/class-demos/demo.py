import psycopg2

connection = psycopg2.connect('dbname=example');

cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS table2;');

cursor.execute('''
create table table2 (
id INTEGER primary key,
completed BOOLEAN NOT NULL DEFAULT False
);
''')

cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (1, True))

SQL = 'INSERT INTO table2 (id, completed) values (%(id)s, %(completed)s);'

data = {
    'id': 2,
    'completed': False
}

cursor.execute(SQL, data)


cursor.execute('SELECT * from table2;')

print('id  |   completed')
print('----|-----------')

for i in cursor.fetchall():
    print(i[0], '  |  ', i[1])
    
cursor.close()
connection.close()
