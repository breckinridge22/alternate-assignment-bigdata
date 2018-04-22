from DB import DB

DB_NAME = 'mlb'

'''
Note: Use triple quotes for multi line queries.

Write SQL queries that return:

1. The number of all stars in allstarsfull.

2. The most home runs in a season by a single player (using the batting table).

3. The playerid of the player with the most home runs in a season.

4. The number of leagues in the batting table.

5. Barry Bond's average batting average (playerid = 'bondsba01') where batting average is hits / at-bats.
Note you will nead to cast hits to get a decimal: cast(h as real)

6. The teamid with the fewest hits in the year 2000 (ie., yearid = '2000').
Return both the teamid, and the number of hits.
Note you can use ORDER BY column and LIMIT 1.

7. The teamid in the year 2000 (i.e., yearid = '2000')  with the highest average batting average.
Return the teamid and the average.
To prevent divsion by 0, limit at-bats > 0.

8. The number of all stars the giants (teamid = 'SFN') had in 2000.

9. The yearid which the giants had the most all stars.

10. The average salary in year 2000.

11. The number of positions (e.g., catchers, pitchers) that have average salaries greather than 2000000 in yearid 2000.
You will need to join fielding with salaries. Also consider using a HAVING clause.

12. The number of errors Barry Bonds had in 2000.

13. The average salary of all stars in 2000.

14. The average salary of non-all stars in 2000.
'''

q1 = 'select count(*) from allstarfull;'

q2 = 'select max(hr) from batting'

q3 = 'select playerid from batting where hr = (select max(hr) from batting)'

q4 = 'select count(distinct lgid) from batting;'

q5 = "select avg(cast(h as real) / ab) from batting where playerid = 'bondsba01';"

q6 = 'select teamid, sum(h) from batting where yearid = 2000 group by teamid order by sum  limit 1 ;'

q7 = '''select teamid, avg(a) from (select cast(h as real) / ab as a, teamid from batting where yearid = 2000 and ab > 0)
T group by teamid order by avg desc;'''

q8 = "select count(*) from allstarfull where teamid = 'SFN' and yearid = '2000'"

q9 = "select yearid from allstarfull where teamid = 'SFN' group by yearid order by count(*)  desc limit 1;"

q10 = "select avg(salary) from salaries where yearid = '2000';"

q11 = '''select count(*) from (select pos from fielding f, salaries s
where s.playerid = f.playerid and f.yearid = '2000' and s.yearid  = '2000' group by
pos having avg(salary) > 2000000) T'''

q12 = "select e from fielding where playerid = 'bondsba01' and yearid = '2000' and e > 0"

q13 = '''select avg(salary) from salaries s, allstarfull a where s.playerid = a.playerid and s.yearid = '2000' and
a.yearid = '2000';'''

q14 = '''select avg(salary) from salaries where yearid = '2000' and playerid NOT IN (select playerid from allstarfull
where yearid = '2000');'''


def main():
    db = DB('mlb')
    for q in [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]:
        for line in db.query(q):
            print line[0]


'''
Sample test case
Note: [0][0] grabs the first field from the first row in the result.
'''


def test_q1():
    db = DB(DB_NAME)
    assert db.query(q1)[0][0] == 5069


def test_q2():
    db = DB(DB_NAME)
    assert db.query(q2)[0][0] == 73


def test_q3():
    db = DB(DB_NAME)
    assert db.query(q3)[0][0] == 'bondsba01'


def test_q4():
    db = DB(DB_NAME)
    assert db.query(q4)[0][0] == 7


def test_q5():
    db = DB(DB_NAME)
    assert db.query(q5)[0][0] == 0.298305762860046


def test_q6():
    db = DB(DB_NAME)
    assert db.query(q6)[0][0] == 'MIL'
    assert db.query(q6)[0][1] == 1366


def test_q7():
    db = DB(DB_NAME)
    assert db.query(q7)[0][0] == 'SEA'
    assert db.query(q7)[0][1] == 0.280799158489005


def test_q8():
    db = DB(DB_NAME)
    assert db.query(q8)[0][0] == 2


def test_q9():
    db = DB(DB_NAME)
    assert db.query(q9)[0][0] in ['1961', '1962']


def test_q10():
    db = DB(DB_NAME)
    assert int(db.query(q10)[0][0]) == 1992984


def test_q11():
    db = DB(DB_NAME)
    assert db.query(q11)[0][0] == 2


def test_q12():
    db = DB(DB_NAME)
    assert db.query(q12)[0][0] == 3


def test_q13():
    db = DB(DB_NAME)
    assert int(db.query(q13)[0][0]) == 5388841


def test_q14():
    db = DB(DB_NAME)
    assert int(db.query(q14)[0][0]) == 1692309


if __name__ == '__main__':
    main()
