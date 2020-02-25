class Library:
	def __init__(self, id, books, signup_time, scanns_per_day):
		self.id = id
		self.books = books
		self.signup_time = signup_time
		self.scanns_per_day = scanns_per_day
		self.metric = None

class Book:
	def __init__(self, id, score):
		self.id = id
		self.score = score
		self.counter = 0


books = []
libraries = []


def find_sum(library):
	sum_of_points = 0
	for book_id in library.books:
		sum_of_points = sum_of_points + books[book_id].score
	return sum_of_points


for file_name in {"a", "b", "c", "d", "e", "f"}:
	libraries = []

	with open(file_name + "_in.txt") as f:
		number_of_books, number_of_libraries, days = [int(x) for x in next(f).split()] # read first line
		scores = [int(x) for x in next(f).split()]
		# print(scores)
		for i in range(len(scores)):
			books.append(Book(i, scores[i]))

		library_id = 0
		for line in f: # read rest of lines
			number_of_books, signup_time, scanns_per_day = [int(x) for x in line.split()]
			books_in_library = [int(x) for x in next(f).split()] # read first line
			books_in_library = list(set(books_in_library))
			new_library = Library(library_id, books_in_library, signup_time, scanns_per_day)
			library_id = library_id + 1
			libraries.append(new_library)
			if library_id == number_of_libraries:
				break

	f.close()


	for library in libraries:
		for book_id in library.books:
			books[book_id].counter += 1

	for library in libraries:
		sum_of_counters = 0
		for book_id in library.books:
			sum_of_counters += books[book_id].counter
		library.metric = sum_of_counters/len(library.books)


	queue_libraries = []
	queue_books = []


	# main

	books_scanned = {}

	until_next_sign_up = 0
	sum_days = 0
	sorted_libraries = sorted(libraries, key=lambda x: (x.signup_time, find_sum(x)) )

	while sum_days < days  and len(sorted_libraries) > 0:
		books_list = sorted(sorted_libraries[0].books, key=lambda x: books[x].score, reverse=True)
		new_books_list = []
		for i in range(len(books_list)):
			if books_list[i] not in books_scanned:
				new_books_list.append(books_list[i])
				books_scanned[books_list[i]] = True
				if sum_days + sorted_libraries[0].signup_time + len(new_books_list)/sorted_libraries[0].scanns_per_day >= days:
					break
		
		if len(new_books_list) > 0:
			queue_libraries.append(sorted_libraries[0])
			queue_books.append(new_books_list)
			sum_days += sorted_libraries[0].signup_time
		
		sorted_libraries.pop(0)



	file1 = open(file_name + "_out.txt","w")
	file1.write(str(len(queue_libraries))+"\n")

	for i in range(0, len(queue_libraries)):
		file1.write(str(queue_libraries[i].id)+" "+str(len(queue_books[i]))+"\n")
		all_books = ""
		my_list = queue_books[i]
		for j in range(0, len(queue_books[i])):
			all_books += str(my_list[j]) + " "
		file1.write(str(all_books)+"\n")
	file1.close()

	print("Sum days: " + str(sum_days) + "/ Days: " + str(days))
