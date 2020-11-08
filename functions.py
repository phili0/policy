import sqlite3 as sq
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import json
from tkinter import messagebox 
from tkinter import *
import os
import datetime


main_data_base='main.db'

m_colors={}




def start_mw(mw): #mw = (main window)
	check_mw_db()
	view_products(mw)
	view_material_types(mw)
	view_rm_units(mw)
	view_rms(mw)
	view_order_colors(mw)
	view_products_rm_units(mw)
	view_all_orders(mw)

	

	f1=partial(add_product,mw)
	mw.add_product.clicked.connect(f1)	

	f2=partial(view_product,mw)
	mw.products_list.clicked.connect(f2)	

	f3=partial(delete_product_f,mw)
	mw.delete_product.clicked.connect(f3)	

	f4=partial(edit_product_f,mw)
	mw.edit_product.clicked.connect(f4)	

	f5=partial(add_unit_f,mw)
	mw.add_unit.clicked.connect(f5)		

	f6=partial(view_unit,mw)
	mw.units_list.clicked.connect(f6)

	f7=partial(delete_unit,mw)
	mw.delete_unit.clicked.connect(f7)

	f8=partial(edit_unit,mw)
	mw.edit_unit.clicked.connect(f8)

	f9=partial(view_rm_units,mw)
	mw.r_matiral_type.currentIndexChanged.connect(f9)

	f10=partial(add_rm,mw)
	mw.add_rm.clicked.connect(f10)

	f11=partial(view_rm,mw)
	mw.rm_list.clicked.connect(f11)

	f12=partial(edit_rm,mw)
	mw.edit_rm.clicked.connect(f12)

	f13=partial(delete_rm,mw)
	mw.delete_rm.clicked.connect(f13)

	f14=partial(add_p_rm,mw)
	mw.add_p_rm.clicked.connect(f14)

	f15=partial(view_product_rm,mw)
	mw.p_rm_list.clicked.connect(f15)

	f16=partial(view_p_rm_m_unit,mw)
	mw.p_rm_combo.currentIndexChanged.connect(f16)

	f17=partial(add_product_order,mw)
	mw.add_order.clicked.connect(f17)

	f18=partial(delete_product_order,mw)
	mw.delete_order.clicked.connect(f18)

	f19=partial(edit_product_order,mw)
	mw.edit_order.clicked.connect(f19)

	f20=partial(view_product_order,mw)
	mw.orders_list.clicked.connect(f20)

	f21=partial(delete_product_rm,mw)
	mw.delete_p_rm.clicked.connect(f21)

	f22=partial(edit_p_rm,mw)
	mw.edit_p_rm.clicked.connect(f22)

	f23=partial(view_products_rm_units,mw)
	mw.p_rm_combo.currentIndexChanged.connect(f23)

def check_mw_db():
	con=sq.connect(main_data_base)
	tables=con.execute("SELECT name FROM sqlite_master WHERE type ='table' ").fetchall()
	if ('products',) not in tables:
		con.execute('''create table products (id integer primary key autoincrement,name,code,material_type)''')


	if ('raw_materials',) not in tables:
		con.execute('create table raw_materials (id integer primary key autoincrement,name,type,code,quantity,unit) ')

	if ('product_raw_materials',) not in tables:
		con.execute('create table product_raw_materials (id integer primary key autoincrement,product_id,material_id,t_quantity,t_unit,m_quantity,m_unit, percentage) ') # t_quantity = total quantity | m_quantity = material quantity

	if ('orders',) not in tables:
		con.execute('create table orders (id integer primary key autoincrement,name,product_id,quantity,unit_id,done,color,date_from,date_to) ') 

	if ('material_types',) not in tables:	
		con.execute('create table material_types (id integer primary key autoincrement,type,units_ids) ')
		con.execute(f"insert into material_types (type,units_ids) values ('Solid','1')")
		con.execute(f"insert into material_types (type,units_ids) values ('Solid','2')")
		con.execute(f"insert into material_types (type,units_ids) values ('Solid','3')")
		con.execute(f"insert into material_types (type,units_ids) values ('Solid','4')")

		con.execute(f"insert into material_types (type,units_ids) values ('Liquid',	'5')")
		con.execute(f"insert into material_types (type,units_ids) values ('Liquid',	'6')")

		con.execute(f"insert into material_types (type,units_ids) values ('Gas','5')")
		con.execute(f"insert into material_types (type,units_ids) values ('Gas','6')")
		con.commit()




	if ('units',) not in tables:	
		con.execute('''create table units (id integer primary key autoincrement , name , product_id , value,unit_id , is_standard )''')


		units=[

			["Milligram  (mg)"	,-1	,1			,'base'	,1],
			["Gram       (g)"  	,-1	,1000		,1		,1],
			["Kilogram   (kg)"	,-1	,1000000	,1		,1],
			["Tonne      (t)"	,-1	,1000000000	,1		,1],
			["Liter      (l)"	,-1	,1			,'base'	,1],
			["Milliliter (ml)"	,-1	,1000		,6		,1]


		]
		for unit in units:

			con.execute('insert into units (name,product_id,value,unit_id,is_standard) values ("{}","{}","{}","{}","{}")'.format(unit[0],unit[1],unit[2],unit[3],unit[4]))
		con.commit()


	con.close()

def view_material_types(mw):
	con=sq.connect(main_data_base)
	types=con.execute('SELECT type,id from material_types').fetchall()
	
	for m_type in types:
		mw.matiral_type.addItem(m_type[0],m_type[1])
		mw.r_matiral_type.addItem(m_type[0],m_type[1])
		types.remove(m_type)
		for m in types:
			if m[0]==m_type[0]:
				types.remove(m)

def view_rm_units(mw):
	con=sq.connect(main_data_base)
	s_units=tuple([ int(i[0]) for i in  con.execute(f'select units_ids from material_types where type="{mw.r_matiral_type.currentText()}" ').fetchall()])
	units =con.execute(f'select * from units where id in {s_units}')
	mw.rm_units_combo.clear()
	for unit in units:
		mw.rm_units_combo.addItem(unit[1],unit[0])

def clear_product_info(mw):
	mw.product_name.setText('')
	mw.product_code.setText('')
	mw.units_list.clear()
	mw.units_combo.clear()
	clear_unit_info(mw)

def clear_unit_info(mw):
	mw.unit_name.setText('')
	mw.unit_value.setValue(0.0)

def clear_rm_info(mw):
	mw.material_name.setText('')
	mw.material_code.setText('')
	mw.rm_quantity.setValue(0.0)

def view_products(mw):
	



	con=sq.connect(main_data_base)
	products=con.execute('SELECT * FROM products').fetchall()
	mw.products_list.clear()
	for product in products:
			#######################
			#######################
			###### item data ######
			#######################
			###	1.icon			###
			###	2.title			###
			###	3.tooltip		###
			###	4.id 			###
			#######################
			#######################
			


		mw.item = QtWidgets.QListWidgetItem()
		mw.item.setData(2,product[1]+'	('+product[2]+')')
		mw.item.setData(4,product[0])
		mw.products_list.addItem(mw.item)
	con.close()

def view_product(mw):
		mw.units_frame.setEnabled(1)
		mw.delete_product.setEnabled(1)
		mw.edit_product.setEnabled(1)

		
		clear_product_info(mw)
		mw.p_rm_t_unit.clear()
		con=sq.connect(main_data_base)
		item=con.execute(f'SELECT * FROM products where id=={mw.products_list.currentItem().data(4)}').fetchall()[0]

		mw.product_name.setText(item[1])
		mw.product_code.setText(item[2])
		
		mw.matiral_type.setCurrentText(item[3])
		
		units=con.execute(f'select * from units where product_id="{mw.products_list.currentItem().data(4)}"').fetchall()
		for unit in units:
			mw.units_combo.addItem(unit[1],unit[0])
			mw.p_rm_t_unit.addItem(unit[1],unit[0])

			mw.item = QtWidgets.QListWidgetItem()
			mw.item.setData(2,unit[1])
			mw.item.setData(4,unit[0])


			mw.units_list.addItem(mw.item)

		s_units=tuple([ int(i[0]) for i in  con.execute(f'select units_ids from material_types where type="{item[3]}" ').fetchall()])
		units =con.execute(f'select * from units where id in {s_units}')
		for unit in units:
			mw.units_combo.addItem(unit[1],unit[0])
			
			mw.p_rm_t_unit.addItem(unit[1],unit[0])
		view_product_rms(mw)
		view_p_rm_m_unit(mw)
		view_product_orders(mw)

def delete_product_f(mw):
	if mw.products_list.currentRow() >= 0:
		master = Tk()
		master.withdraw()
		m=messagebox.askquestion("Delete product", f"do you realy want to delete this product?") 
		print(m)
		if m=='yes':
			clear_product_info(mw)
			con=sq.connect(main_data_base)
			c_i=mw.products_list.currentIndex()
			con.execute(f''' DELETE FROM products where id=={mw.products_list.currentItem().data(4)} ''')
			con.commit()
			view_products(mw)
			#if mw.products_list.count()-1>=c_i:
			#	mw.products_list.setCurrentIndex(c_i)
			#else:
			#	mw.products_list.setCurrentIndex(c_i-1)

	else:
			
		master = Tk()
		master.withdraw()
		m=messagebox.showinfo("No selected item", "please select item to delete it") 

def edit_product_f(mw):
	
	if mw.products_list.currentRow() >= 0:
		con=sq.connect(main_data_base)
		con.execute(f''' update products set 	name='{mw.product_name.text()}' ,
		 										code='{mw.product_code.text()}'
												  where id=={mw.products_list.currentItem().data(4)} ''')
		con.commit()
		view_products(mw)
		clear_product_info(mw)
	else:
			
		master = Tk()
		master.withdraw()
		m=messagebox.showinfo("No selected item", "please select item to edit it") 

def add_product(mw):
	con=sq.connect(main_data_base)
	ch=con.execute(f'select name from products where name="{mw.product_name.text()}"').fetchall()
	m=True
	if len(ch)>0:
		master = Tk()
		master.withdraw()
		m=messagebox.askquestion("Add product", f"There are {len(ch)} product with name '{ch[0][0]}' \n do you still want to add this product? ") 

	if m:
		con.execute("INSERT into products (name,'code','material_type') values ('"+mw.product_name.text()+"','"+mw.product_code.text()+"','"+str(mw.matiral_type.currentText())+"') ")
		con.commit()
		view_products(mw)
		clear_product_info(mw)

def add_unit_f(mw):
	if mw.products_list.currentRow() >= 0:
		con=sq.connect(main_data_base)
		con.execute(f'insert into units (name,product_id,value,unit_id,is_standard) values ("{mw.unit_name.text()}","{mw.products_list.currentItem().data(4)}","{mw.unit_value.value()}","{mw.units_combo.itemData(mw.units_combo.currentIndex())}",0)')
		con.commit()
		view_product(mw)
		clear_unit_info(mw)
	else:
			
		master = Tk()
		master.withdraw()
		m=messagebox.showinfo("No selected product", "please select a product to add new unit") 

def view_unit(mw):
	con=sq.connect(main_data_base)
	mw.unit_name.setText(mw.units_list.currentItem().text())
	
	data=con.execute(f" select value,unit_id from units where id='{mw.units_list.currentItem().data(4)}' ").fetchall()[0]
	
	unit_f=con.execute(f" select name from units where id='{data[1]}' ").fetchall()[0][0]

	mw.unit_value.setValue(float(data[0]))
	mw.units_combo.setCurrentText(unit_f)

def delete_unit(mw):
	if mw.units_list.currentRow() >= 0:
		master = Tk()
		master.withdraw()
		m=messagebox.askquestion("Delete product", f"do you realy want to delete this unit?") 
		if m=='yes':
			con=sq.connect(main_data_base)
			m=''
			r_units=con.execute(f'select * from units where unit_id="{mw.units_list.currentItem().data(4)}" ').fetchall()
			if len(r_units)>0:
				master = Tk()
				master.withdraw()
				m=messagebox.askquestion("Delete unit", f"this unit is base for {len(r_units)} other units \n do you want to delete all this units?") 



			if m=='yes' or len(r_units)==0:

					con.execute(f'delete from units where id={mw.units_list.currentItem().data(4)}')
					con.execute(f'delete from units where unit_id="{mw.units_list.currentItem().data(4)}"')
					con.commit()
					clear_unit_info(mw)
					view_product(mw)

	else:
		master = Tk()
		master.withdraw()
		m=messagebox.showinfo("No selected item", "please select item to delete it") 

def edit_unit(mw):
	if mw.units_list.currentRow() >= 0:
		con=sq.connect(main_data_base)
		con.execute(f''' update units set 	name='{mw.unit_name.text()}',
											value='{mw.unit_value.value()}',
											unit_id='{mw.units_combo.itemData(mw.units_combo.currentIndex())}'
											where id='{mw.units_list.currentItem().data(4)}' ''')
		con.commit()
		view_product(mw)
	else:
		master = Tk()
		master.withdraw()
		m=messagebox.showinfo("No selected item", "please select item to edit it") 

def view_p_rm_m_unit(mw):
	con=sq.connect(main_data_base)
	m_type=con.execute(f'select "type" from material_types where id={mw.matiral_type.itemData(mw.matiral_type.currentIndex())}').fetchall()[0][0]
	s_units=tuple([ int(i[0]) for i in  con.execute(f'select units_ids from material_types where type="{m_type}" ').fetchall()])
	units =con.execute(f'select * from units where id in {s_units}')
	mw.order_unit.clear()
	for unit in units:
			mw.order_unit.addItem(unit[1],unit[0])

def add_rm(mw): # rm (Raw material)
	con=sq.connect(main_data_base)
	con.execute(f'insert into raw_materials (name,type,code,quantity,unit) values ("{mw.material_name.text()}","{mw.r_matiral_type.currentText()}","{mw.material_code.text()}","{mw.rm_quantity.value()}","{mw.rm_units_combo.currentText()}") ')
	con.commit()
	view_rms(mw)

def view_rms(mw): # rms (Raw Materials)
	con=sq.connect(main_data_base)
	items=con.execute('select name,quantity,unit,id from raw_materials').fetchall()
	items.sort(key=lambda x:x[0])

	mw.rm_list.clear()
	mw.p_rm_combo.clear()
	for item in items:
		mw.item = QtWidgets.QListWidgetItem()
		unit=item[2].split('(')[1].replace(")","")
		mw.item.setData(2,f'{item[0]}	({item[1]} {unit})')
		mw.item.setData(4,item[3])
		mw.rm_list.addItem(mw.item)

		mw.p_rm_combo.addItem(item[0],item[3])

def view_rm(mw):
	try:
		con=sq.connect(main_data_base)
		item=con.execute(f'select name,type,code,quantity,unit from raw_materials where id=={mw.rm_list.currentItem().data(4)}').fetchall()[0]
		
		mw.material_name.setText(item[0])
		mw.r_matiral_type.setCurrentText(item[1])
		mw.material_code.setText(item[2])
		mw.rm_quantity.setValue(float(item[3]))
		mw.rm_units_combo.setCurrentText(item[4])
	except:
		pass

def edit_rm(mw):
	if mw.rm_list.currentRow() >= 0:
		con=sq.connect(main_data_base)
		con.execute(f'''update raw_materials set name="{mw.material_name.text()}"
												,code="{mw.material_code.text()}"
												,quantity="{mw.rm_quantity.value()}"
												,unit="{mw.rm_units_combo.currentText()}"
													where id=={mw.rm_list.currentItem().data(4)} ''')
		con.commit()
		view_rms(mw)
		clear_rm_info(mw)

	else:
		master = Tk()
		master.withdraw()
		m=messagebox.showinfo("No selected item", "please select item to edit it") 

def delete_rm(mw):
	if mw.rm_list.currentRow() >= 0:
		master = Tk()
		master.withdraw()
		m=messagebox.askquestion("Delete product", f"do you realy want to delete this material?") 
		if m=='yes':
			con=sq.connect(main_data_base)
			con.execute(f'delete from raw_materials where id="{mw.rm_list.currentItem().data(4)}"')
			con.commit()
			view_rms(mw)
			clear_rm_info(mw)
	else:
		master = Tk()
		master.withdraw()
		m=messagebox.showinfo("No selected item", "please select item to delete it") 

def add_p_rm(mw):
	if mw.products_list.currentRow() >= 0:
		con=sq.connect(main_data_base)
		percentages=[ float(i[0]) for i in con.execute(f'select percentage from product_raw_materials where product_id="{mw.products_list.currentItem().data(4)}"').fetchall()]
		total_percentage =0
		for percentage in percentages:
			total_percentage+=percentage

		total_current_value=mw.p_rm_t_quantity.value()*get_unit_value(mw.p_rm_t_unit.itemData(mw.p_rm_t_unit.currentIndex()))
		material_current_value=mw.p_rm_m_quantity.value()*get_unit_value(mw.p_rm_m_unit.itemData(mw.p_rm_m_unit.currentIndex()))
		
		current_percentage=100*material_current_value/total_current_value

		if total_percentage+current_percentage<=100:

			con.execute(f'''insert into product_raw_materials (product_id , material_id , t_quantity , t_unit , m_quantity , m_unit ,percentage) values ("{mw.products_list.currentItem().data(4)}","{mw.p_rm_combo.itemData(mw.p_rm_combo.currentIndex())}","{mw.p_rm_t_quantity.value()}","{mw.p_rm_t_unit.itemData(mw.p_rm_t_unit.currentIndex())}","{mw.p_rm_m_quantity.value()}","{mw.p_rm_m_unit.itemData(mw.p_rm_m_unit.currentIndex())}","{current_percentage}")''')
			con.commit()
			view_product_rms(mw)
		
		else:		
			master = Tk()
			master.withdraw()
			m=messagebox.showinfo("Big quantity", f"you have only {100-total_percentage}% from ptoduct to add raw materials \n you are trying to add {current_percentage}% of {mw.p_rm_combo.currentText()}") 


	else:		
		master = Tk()
		master.withdraw()
		m=messagebox.showinfo("No selected product", "please select a product to add new raw material") 

def edit_p_rm(mw):

	if mw.products_list.currentRow() >= 0:
		con=sq.connect(main_data_base)
		percentages=[ float(i[0]) for i in con.execute(f'select percentage from product_raw_materials where product_id="{mw.products_list.currentItem().data(4)}"').fetchall()]
		total_percentage =0
		for percentage in percentages:
			total_percentage+=percentage

		total_current_value=mw.p_rm_t_quantity.value()*get_unit_value(mw.p_rm_t_unit.itemData(mw.p_rm_t_unit.currentIndex()))
		material_current_value=mw.p_rm_m_quantity.value()*get_unit_value(mw.p_rm_m_unit.itemData(mw.p_rm_m_unit.currentIndex()))
		
		current_percentage=100*material_current_value/total_current_value

		last_percentage=float(con.execute(f'select percentage from product_raw_materials where id="{mw.p_rm_list.currentItem().data(4)}"').fetchall()[0][0])


		if total_percentage+current_percentage-last_percentage<=100:


			con.execute(f'''update product_raw_materials set 
															 material_id ="{mw.p_rm_combo.itemData(mw.p_rm_combo.currentIndex())}"
															, t_quantity ="{mw.p_rm_t_quantity.value()}"
															, t_unit ="{mw.p_rm_t_unit.itemData(mw.p_rm_t_unit.currentIndex())}"
															, m_quantity="{mw.p_rm_m_quantity.value()}" 
															, m_unit="{mw.p_rm_m_unit.itemData(mw.p_rm_m_unit.currentIndex())}"
															, percentage="{current_percentage}"
															 where id={mw.p_rm_list.currentItem().data(4)} ''')
			con.commit()
			view_product_rms(mw)


		else:		
			master = Tk()
			master.withdraw()
			m=messagebox.showinfo("Big quantity", f"you have only {100-total_percentage}% from ptoduct to add raw materials \n you are trying to add {current_percentage-last_percentage}% of {mw.p_rm_combo.currentText()}") 

def view_product_rms(mw):
	con=sq.connect(main_data_base)
	items=con.execute(f'select * from product_raw_materials where product_id="{mw.products_list.currentItem().data(4)}"').fetchall()
	mw.p_rm_list.clear()
	for item in items:
		name=con.execute(f'select name from raw_materials where id={item[2]} ').fetchall()[0][0]
		mw.item = QtWidgets.QListWidgetItem()
		mw.item.setData(2,name+"	"+item[7]+"%")
		mw.item.setData(4,item[0])

		mw.p_rm_list.addItem(mw.item)

def view_product_rm(mw):
		clear_rm_info(mw)
		con=sq.connect(main_data_base)
		item=con.execute(f'select * from product_raw_materials where id="{mw.p_rm_list.currentItem().data(4)}"').fetchall()[0]
		m_name=con.execute(f'select name from raw_materials where id={item[2]}').fetchall()[0][0]
		t_unit=con.execute(f'select name from units where id={item[4]}').fetchall()[0][0]
		m_unit=con.execute(f'select name from units where id={item[6]}').fetchall()[0][0]

		mw.p_rm_combo.setCurrentText(m_name)
		mw.p_rm_t_quantity.setValue(float(item[3]))
		mw.p_rm_t_unit.setCurrentText(t_unit)
		mw.p_rm_m_quantity.setValue(float(item[5]))
		mw.p_rm_m_unit.setCurrentText(m_unit)
		print('dddddd')

def delete_product_rm(mw):
	if mw.p_rm_list.currentRow() >= 0:
		master = Tk()
		master.withdraw()
		m=messagebox.askquestion("Delete order", f"do you realy want to delete this order?") 
		if m=='yes':
			con=sq.connect(main_data_base)
			con.execute(f'delete from product_raw_materials where id={mw.p_rm_list.currentItem().data(4)}')
			con.commit()
			view_product_rms(mw)
	else:
		master = Tk()
		master.withdraw()
		m=messagebox.showinfo("No selected item", "please select item to delete it") 

def view_products_rm_units(mw):
	try:
		con=sq.connect(main_data_base)
		m_type=con.execute(f'select type from raw_materials where id={mw.p_rm_combo.itemData(mw.p_rm_combo.currentIndex())}').fetchall()[0][0]
		s_units=tuple([ int(i[0]) for i in  con.execute(f'select units_ids from material_types where type="{m_type}" ').fetchall()])
		units =con.execute(f'select * from units where id in {s_units}')
		mw.p_rm_m_unit.clear()
		for unit in units:
			mw.p_rm_m_unit.addItem(unit[1],unit[0])
	except:
		pass
			
def view_product_orders(mw):
	con=sq.connect(main_data_base)
	items=con.execute(f' select * from orders where product_id="{mw.products_list.currentItem().data(4)}"')
	mw.orders_list.clear()
	for item in items:
		unit=con.execute(f'select name from units where id={item[4]}').fetchall()[0][0].split('(')[1].replace(")","")
		mw.item = QtWidgets.QListWidgetItem()
		mw.item.setData(2,item[1])
		mw.item.setData(4,item[0])
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(f"icons/colors/{item[6]}.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		
		mw.item.setIcon(icon)
		mw.item.setTextAlignment(QtCore.Qt.AlignCenter)
		mw.orders_list.addItem(mw.item)
		
def view_order_colors(mw):

	colors=(os.listdir('icons/colors'))
	a=0
	for color in colors:
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(f"icons/colors/{color}"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		mw.order_color.addItem(icon, "" ,color.split('.')[0])
		m_colors[color.split('.')[0]]=str(a)
		a+=1

def clear_order_info(mw):
	mw.order_name.setText('')
	mw.order_quantity.setValue(0.0)
	mw.order_done.setChecked(0)

def add_product_order(mw):
	if mw.products_list.currentRow() >= 0:
		con=sq.connect(main_data_base)
		low_material_quantity=[]
		materials_id={}
		order_quantity=mw.order_quantity.value()*get_unit_value(mw.order_unit.itemData(mw.order_unit.currentIndex()))


		for rm in con.execute(f'select material_id,percentage from product_raw_materials where product_id="{mw.products_list.currentItem().data(4)}" ').fetchall():
				materials_id[rm[0]]=rm[1]
				qu=con.execute(f'select name,quantity from raw_materials where id={rm[0]} ').fetchall()[0]
				if float(qu[1])<order_quantity*float(rm[1])/100:
					low_material_quantity.append(qu[0])

		
		if len(low_material_quantity)==0:
			con.execute(f''' insert into orders (name , product_id , quantity , unit_id , color , date_from , date_to) values
							(
							"{mw.order_name.text()}",
							"{mw.products_list.currentItem().data(4)}",
							"{mw.order_quantity.value()}",
							"{mw.order_unit.itemData(mw.order_unit.currentIndex())}",
							"{mw.order_color.itemData(mw.order_color.currentIndex())}",
							"{mw.date_order_from.date().toPyDate()}",
							"{mw.date_order_to.date().toPyDate()}"
							)
							''')
			
			
			for m_id in materials_id.keys():
				qu=float(con.execute(f'select quantity from raw_materials where id={m_id}').fetchall()[0][0])
				new_quantity=qu-mw.order_quantity.value()* float(materials_id[m_id])/100
				con.execute(f'update raw_materials set quantity={new_quantity} where id={m_id} ')
			con.commit()
			view_product_orders(mw)
			view_rms(mw)
			view_all_orders(mw)


		else:		
			master = Tk()
			master.withdraw()
			m=messagebox.showinfo("No enough quantity", f"you have no enough quantity of { ' and '.join(low_material_quantity) }") 

	else:		
		master = Tk()
		master.withdraw()
		m=messagebox.showinfo("No selected product", "please select a product to add new order") 

def delete_product_order(mw):
	master = Tk()
	master.withdraw()
	m=messagebox.askquestion("Delete order", f"do you realy want to delete this order?") 
	if m=='yes':
		con=sq.connect(main_data_base)
		con.execute(f''' delete from orders where id={mw.orders_list.currentItem().data(4)}''')
		con.commit()
		view_product_orders(mw)
		view_all_orders(mw)

def edit_product_order(mw):
	con=sq.connect(main_data_base)
	con.execute(f''' update orders set
					name="{mw.order_name.text()}",
					quantity="{mw.order_quantity.value()}",
					unit_id="{mw.order_unit.itemData(mw.order_unit.currentIndex())}",
					color="{mw.order_color.itemData(mw.order_color.currentIndex())}",
					date_from="{mw.date_order_from.date().toPyDate()}",
					date_to="{mw.date_order_to.date().toPyDate()}"
					
					where id={mw.orders_list.currentItem().data(4)}
					''')
	con.commit()
	view_product_orders(mw)

def view_product_order(mw):
	con=sq.connect(main_data_base)
	item=con.execute(f' select * from orders where id={mw.orders_list.currentItem().data(4)}').fetchall()[0]
	unit=con.execute(f' select name from units where id={item[4]}').fetchall()[0][0]

	mw.order_name.setText(item[1])
	mw.order_quantity.setValue(float(item[3]))
	mw.order_unit.setCurrentText(unit)
	mw.order_color.setCurrentIndex(int(m_colors[item[6]]))
	mw.date_order_from.setDate(datetime.date.fromisoformat(item[7]))
	mw.date_order_to.setDate(datetime.date.fromisoformat(item[8]))
					
def get_unit_value(unit_id):
	con=sq.connect(main_data_base)
	unit_value=1

	while True:
		try:
			unit=con.execute(f'select value,unit_id  from units where id={unit_id}').fetchall()[0]
			unit_value=unit_value*float(unit[0])
			if unit[1]=='base':
				break
			else:
				unit_id=int(unit[1])
		except:
			print(int(unit_id))

	return unit_value

def view_all_orders(mw):
	con=sq.connect(main_data_base)
	products=con.execute('select name,id from products').fetchall()

	mw.all_orders.setColumnCount(0)
	mw.all_orders.setRowCount(0)

	
	
	for product in products:
		mw.all_orders.setRowCount(mw.all_orders.rowCount()+1)

		item = QtWidgets.QTableWidgetItem()
		item.setText(product[0])
		mw.all_orders.setVerticalHeaderItem(mw.all_orders.rowCount()-1, item)

		orders=con.execute(f'select * from orders where product_id="{product[1]}"').fetchall()
		if len(orders)>mw.all_orders.columnCount():
			b=1
			for i in range(len(orders)-mw.all_orders.columnCount()):
				item = QtWidgets.QTableWidgetItem()
				mw.all_orders.setHorizontalHeaderItem(mw.all_orders.columnCount()+b , item)
				b+=1

			mw.all_orders.setColumnCount(len(orders))

		y=0	
		for order in orders:
			item = QtWidgets.QTableWidgetItem()
			item.setText(order[1])
			color=order[6].split(',')
			brush = QtGui.QBrush(QtGui.QColor(int(color[0]),int(color[2]),int(color[2])))
			brush.setStyle(QtCore.Qt.SolidPattern)
			item.setBackground(brush)

			mw.all_orders.setItem(mw.all_orders.rowCount()-1 , y, item)
			y+=1

		




        #item = QtWidgets.QTableWidgetItem()
        #self.all_orders.setVerticalHeaderItem(0, item)




		#item = QtWidgets.QTableWidgetItem()
		#mw.all_orders.setHorizontalHeaderItem(2, item)



		#item = QtWidgets.QTableWidgetItem()
		#mw.all_



        #item = QtWidgets.QTableWidgetItem()
        #self.all_orders.setItem(0, 0, item)