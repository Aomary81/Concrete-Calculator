#!/usr/bin/python3
import math
import sqlite3  
import time


connection = sqlite3.connect("jobs.db")  
c = connection.cursor()                      
def create_table():
  sql_obj = """create table if not exists jobs( jname VARCHAR(20) NOT NULL,  yardage REAL, concretePrice REAL, posts INTEGER, totalCost REAL, date DATE );"""

  sql_obj2 = """create table if not exists posts( jname2 VARCHAR(20) NOT NULL, postShape char(5),postSize INT, postDepth INT, holeWidth INT, holeDepth INT, posts2 INT, yardage2 REAL, concretePrice2 REAL, totalCost2 REAL, date2 DATE );"""
  c.execute(sql_obj)
  c.execute(sql_obj2)
  connection.commit()

def rPosts_volume(diameter, length):
  radius = diameter/2
  area = math.pi * radius * radius
  volume = area * length
  return volume

def sPosts_volume(side, length):
  area = side ** 2
  volume = area * length
  return volume

def postHole(diameter, depth):
  radius = diameter/2
  area = math.pi * radius * radius
  volume = area * depth
  return volume

def concret_volume(post, hole):
  total = hole - post
  return total

def yardage(quantity, volume):
  cubic_inches = quantity * volume
  yards = cubic_inches / 46656 
  return yards

def total_cost(quantity, cost):
  total = quantity * cost
  return total

create_table()              
jobName = input("What is the name of this Job: ")
concreteCost = float(input("What is your cost per yard of concrete? "))
localtime = time.asctime( time.localtime(time.time()) )
tQuantity = 0
i = 0
r_concrete =0
s_concrete =0
d_posts = int(input("How many different size posts do you have? "))
while i < d_posts:
  print("Is your post ROUND or SQUARE? ")
  shape = input(" r for ROUND and s for SQUARE ") 
  if shape in ['r', 'R','round','ROUND']:
    pDia = float(input("What is the diameter of your post (inches)? "))
    pLength = float(input("How much post is in the ground (inches)? "))
    pQuantity = int(input("How many post do you have? "))
    hDia = float(input("What is the diameter of your posthole (inches)? "))
    hDepth= float(input("How deep is your post hole (inches)? "))
    rPostV = rPosts_volume(pDia, pLength)
    rPostH = postHole(hDia, hDepth)
    rPostC = concret_volume(rPostV, rPostH)
    tQuantity = tQuantity + pQuantity
    r_concreteV = yardage(pQuantity,rPostC)
    r_concrete = r_concrete + r_concreteV
    rCost = total_cost(r_concreteV,concreteCost)
    i = i+1
    c.execute ("insert into posts(jname2,postShape,postSize,postDepth,holeWidth,holeDepth,posts2,yardage2,concretePrice2,totalCost2,date2) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (jobName,shape,pDia,pLength,hDia,hDepth,pQuantity,round(r_concreteV,2),concreteCost,round(rCost,2),localtime) )
  elif  shape in ['s', 'S', 'square','SQUARE']:
    pSize = float(input("What is the size of your post (inches)? "))
    pLength = float(input("How much post is in the ground (inches)? "))
    pQuantity = int(input("How many post do you have? "))
    hDia = float(input("What is the diameter of your posthole (inches)? "))
    hDepth= float(input("How deep is your post hole (inches)? "))
    sPostV = sPosts_volume(pSize, pLength)
    sPostH = postHole(hDia, hDepth)
    sPostC = concret_volume(sPostV, sPostH)
    tQuantity = tQuantity + pQuantity
    s_concreteV = yardage(pQuantity,sPostC)
    s_concrete = s_concrete + s_concreteV
    sCost = total_cost(s_concreteV,concreteCost)
    i = i +1
    c.execute ("insert into posts(jname2,postShape,postSize,postDepth,holeWidth,holeDepth,posts2,yardage2,concretePrice2,totalCost2,date2) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (jobName,shape,pSize,pLength,hDia,hDepth,pQuantity,round(s_concreteV,2),concreteCost,round(sCost,2),localtime) )
  else:
    print("Post shape not recognized, please use r for ROUND or s for SQUARE.")


t_concrete = r_concrete + s_concrete
tCost = total_cost(t_concrete,concreteCost)
c.execute ("insert into jobs(jname,yardage,concretePrice,posts,totalCost,date) values (?,?,?,?,?,?)", (jobName,round(t_concrete,2),concreteCost,tQuantity,round(tCost,2),localtime))
connection.commit()

c.execute("select * from jobs")
result= c.fetchall()
for i in result:
    print(i)
print()

c.execute("select * from posts")
result= c.fetchall()
for i in result:
    print(i)

