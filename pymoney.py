import sys
import os

file_name = "records.txt"

class Record:
	"""
	Represent a record
	"""
	
	def __init__(self, cat, des, amt):
		"""
		create a record
		"""
		self._cat = cat
		self._des = des
		self._amt = amt
	
	@property
	def category(self):
		return self._cat
	
	@property
	def description(self):
		return self._des
	
	@property
	def amount(self):
		return self._amt

class Categories:
	"""
	Records category information
	"""

	def __init__(self, ini_value = None):
		"""
		initialize category list
		"""
		if ini_value == None:
			self._list = ['expense', ['food', ['meal', 'snack', 'drink', 'groceries'], 'transportation', 'entertainment', ['album', 'concert', 'movie'], 'digital', ['subscription', 'maintenance']],'income', ['salary', 'scholarship', 'allowance']]

		else:
			self._list = eval(ini_value)
	

	def view(self):
		"""
		view categories in layer order
		"""
		
		def view_rec(cats, lv):
			for c in cats:
				if type(c) != list:
					print(f"{' '*2*lv}- {c}")
				else:
					view_rec(c, lv+1)
			if lv == 0:
				print()
		
		view_rec(self._list, 0)
	
	def is_category_valid(self, cat):
		"""
		check if category is a valid input
		"""
		L = self._flatten()
		return cat in L
		
	def flatten(self, cats):
		if type(cats) == list:
			result = []
			for c in cats:
				result.extend(self.flatten(c))
			return result
		else:
			return [cats]
	
	def find_subcategories(self, cat):
		"""
		find all subcategories
		"""
		def find_subcategories_gen(cat, cats, found=False):
			if type(cats) == list:
				for c in cats:
					yield from find_subcategories_gen(cat, c, found)
					if c == cat and cats.index(c)+1 < len(cats) and \
					type(cats[cats.index(c)+1]) == list:
						yield from find_subcategories_gen(cat, cats[cats.index(c)+1], True)

			else:
				if cats == cat or found == True:
					yield cats

		cat_list_gen = find_subcategories_gen(cat, self._list)
		cat_list_ret = []
		item = next(cat_list_gen, None)
		while item != None:
			cat_list_ret.append(item)
			item = next(cat_list_gen, None)
		
		return cat_list_ret
	
	def _flatten(self):
		"""
		flatten the category list
		"""

		return self.flatten(self._list)
	
	@property
	def val(self):
		"""
		return the list
		"""

		return self._list
	
	def add(self, cat, pos):
		"""
		add a new category
		"""

		self._list[pos].append(cat)


class Records:
	"""
	Maintain a list of all the 'Record's and the initial amount of money
	"""

	def __init__(self):
		"""
		record all the information
		"""
		try:
			fh = open(file_name)
			print("Welcome Back!!\n")
			ttl_s = fh.readline()

			if ttl_s == '':
				print("\n##### error with file #####")
				print("reason: empty file")
				print("let's start from the beginning...\n")
				self._ttl = self.prompt_input()
			
			else:
				# read total money
				try:
					self._ttl = int(ttl_s)
				except:
					print("\n##### error with file #####")
					print("reason: unable to read in total amount")
					print("records will be saved if under right format...\n")
					self._ttl = self.prompt_input()
				
				# read category list
				try:
					self._cat_list = Categories(fh.readline())
				except:
					print("\n##### error with file #####")
					print("reason: unable to read in category list")
					print("going with default categories...\n")
					self._cat_list = Categories()

				# read records
				lst = fh.readlines()
				fh.close()
				self._list = []
				for l in lst:
					try:
						l = l[:-1]
						cat, des, amt_s = l.split()
						amt = int(amt_s)
						self._list.append(Record(cat, des, amt))
					except:
						print("\n##### error with file #####")
						print("reason: wrong record format")
						print(f"skipping record <{l}> ...\n")
		except:
			print("\n##### starting over #####")
			print("reason: records.txt file not found")
			print("creating a new file...\n")
			self._list = []
			self._cat_list = Categories()
			self._ttl = self.prompt_input()
	
	def prompt_input(self):
		"""
		prompt initial value if there isn't one
		"""
		
		ttl_s = input("How much money do you have? ")
		try:
			ttl = int(ttl_s)
			return ttl
		except:
			print("\n##### input error #####")
			print("reason: wrong input format")
			print("please enter an integer...\n")
			return self.prompt_input()
	
	def add(self):
		"""
		add new records
		"""
		
		lst = input("Add an expense or income record with category, description and amount\n>>>format: cat-1 des-1 amt-1, cat-2 des-2 amt-2, ...\n").split(', ')
		Amt = "all"
		for l in lst:
			try:
				cat, des, amt_s = l.split()
				amt = int(amt_s)
				self._ttl += amt
				self._list.append(Record(cat, des, amt))
				if not self._cat_list.is_category_valid(cat):
					if amt < 0:
						self._cat_list.add(cat, 1)
						top_cat = 'expense'
					else:
						self._cat_list.add(cat, 3)
						top_cat = 'income'
					print("\n##### new category #####")
					print("new category found")
					print(f"adding category <{cat}> to <{top_cat}>...\n")
			except:
				print("\n##### input error #####")
				print("reason: wrong input format")
				print(f"skipping record <{l}> ...\n")
				Amt = "part of the"
			

		print(f"{Amt} records saved\n")

	def view(self):
		"""
		display all records
		"""

		print("Here's your expense and income records:\n")
		print("idx  Category          Description           Amount")
		print("===  ================  ====================  ======")
		for i, l in enumerate(self._list):
			print(f"{(i+1):3d}  {l.category:16}  {l.description:20s}  {l.amount:+6d}")
		print("===  ================  ====================  ======")
		print(f"Now you have {self._ttl} dollars.\n")
	
	def delete(self):
		"""
		delete unwanted record
		"""

		num_s = input("Which record do you want to delete?\n>>>format: [idx]\n")
		try:
			num = int(num_s)
			if num > len(self._list):
				print("\n##### input error #####")
				print(f"reason: index out of range [1:{len(self._list)}]")
				print("exitting <delete> and try again...\n")
				return
			self._ttl -= self._list[num-1].amount
			print("ok")
			self._list.pop(num-1)
		except:
			print("\n##### input error #####")
			print("reason: not an integer index")
			print("exitting <delete> and try again...\n")
			return
	
	def find(self):
		"""
		find records under a certain category
		"""

		cat = input("Which category do you want to find?\n>>>format: [category]\t")
		cat_list = self._cat_list.find_subcategories(cat)
		if cat_list == []:
			print(f"category <{cat}> not found\n")
			return
		i, ttl = 1, 0
		new_list = list(filter(lambda x: x.category in cat_list, self._list))
		print(f"\n{cat}:")
		print("idx  Category          Description           Amount")
		print("===  ================  ====================  ======")
		for i, l in enumerate(new_list):
			print(f"{i+1:3d}  {l.category:16}  {l.description:20}  {l.amount:+6d}")
			ttl += l.amount
		print("===  ================  ====================  ======")
		print(f"The total amount above is {ttl}\n")

	def save(self):
		"""
		save records to file and turn it into read-only
		"""

		try:
			os.chmod(file_name, 0o666)
		except:
			pass
		fh = open(file_name, 'w')
		fh.write(f"{self._ttl}\n")
		fh.write(f"{self._cat_list.val}\n")
		for l in self._list:
			fh.write(f"{l.category} {l.description} {l.amount}\n")
		print("\nsaving...\ndone!")
		os.chmod(file_name, 0o444)

if __name__ == '__main__':
	rec = Records()

	while True:
		command = input("What do you want to do (add / view / delete / view categories / find / exit)? ")
		if command == "add":
			rec.add()
		elif command == "view":
			rec.view()
		elif command == "delete":
			rec.delete()
		elif command == "view categories":
			rec._cat_list.view()
		elif command == "find":
			rec.find()
		elif command == "exit":
			rec.save()
			break
		else:
			sys.stderr.write("Invalid command. Try again.\n")
