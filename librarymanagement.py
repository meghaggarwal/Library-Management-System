import sys, os
import pandas as pd

class Library:

    def __init__(self, listofbooks, libraryname):
        self.lendedbooks = {}
        self.listofbooks = listofbooks
        self.libraryname = libraryname
        
        for key , value in self.listofbooks.items():
           self.lendedbooks[(key, value)] = 'None'
           
        Library.update_total_books(self)
           
    def update_total_books(self):
        '''Updates the total no of books in the library present'''
        displaybooks = {}
        for value in self.listofbooks.values():
            if value in displaybooks:
                displaybooks[value] += 1
            else:
                displaybooks[value] = 1
        available_books = displaybooks.values()
        self.df = pd.DataFrame(available_books, displaybooks.items(), columns = ['Total No of Books'])
        self.df.reset_index(inplace = True)
        self.df.index.name = 'Sl No'
        self.df.columns = ['Book Name' , 'Total No of Books', 'Available Books']
       
   
        
      

    def display(self): 
        '''Show the books in the library issued as well as not taken by the student'''
         
        self.df1 = pd.DataFrame(self.lendedbooks.values(), self.lendedbooks.keys() )
        self.df1.reset_index(inplace = True)
        self.df1.index.name = 'SL No'
        self.df1.columns = ['QR CODE', 'Book Name', 'Student Name'] 
        self.taken = self.df1[self.df1['Student Name'] != 'None']
        self.not_taken = self.df1[self.df1['Student Name'] == 'None']
        print(f"The books present along with the no of books:\n {self.df}")
        print(f"List of the books taken by the student:\n {self.taken}")
        print(f"List of the books not taken by the student:\n {self.not_taken.iloc[:,0:2]}")
   
        
    def borrow(self): 
        '''Issue a book to the student'''
        borrowdic = {}
        lend = False
        bname = input(f"Enter the name of the book required from list:\n{self.df}\n")
        present = False
        for score , bookname in self.listofbooks.items(): #If book is there in library or not
            if bname == bookname: 
                borrowdic[score] = bname #Shows the books that are present with the same name
                present = True
                
        #Now we want to see the qrcode of the book that will be given to student with the list of books available.
        if present:
                pname = input('Enter the name of the student: ')
        else:
            print('Retry the book-name not available')
         
        #borrowdic contains the list of total books in library with same name
        #Now we want to see the qrcode of the book that will be given to student with the list of books available (not lended).
        if borrowdic:
            
            for scancode, value in borrowdic.items():
                if self.lendedbooks[(scancode , value)] is 'None':
                    self.lendedbooks[(scancode, value)] = pname
                    lend = True
                    self.df.loc[self.df['Book Name'] == bname,  'Available Books'] -=1
                    print('the book is sucessfully given')
                    break
                    
            if lend is False:
               
                print('The book is taken by someone else')

                              
        
    def submit(self): 
        '''Return the borrowed book back to the store'''
        scancode = []
        pname = input("Enter the name of the person who want to return the book: ")
        bname = input("Enter the book name: ")
        scancode = input('Scan the code of the book to be returned: ')
        if scancode in self.listofbooks and bname in self.listofbooks[scancode]:  #Scan the book if it belongs to the library
            if self.lendedbooks[(scancode, bname)] == pname: #if book was actually borrowed by the student
                self.lendedbooks.pop((scancode, bname))
                self.df.loc[self.df['Book Name'] == bname,  'Available Books'] +=1
                print(f' The {bname} was returned successfully')
            else:
                print('The student did not actually borrowed the book')
        else:
            print('The book does not belong the library')
            
    def addbooks(self): 
        '''Add new book to the library store'''
        bname = input('Enter the name of the book: ')
        scancode = input('Enter the ISBN code of the book: ')
        insert = False
        for qr, name in self.listofbooks.items():
            if scancode == qr:
                print('Invalid QRCODE , same qr code is already in the store')
                insert = False
                
            else:
                insert = True
             
        if insert:
            self.listofbooks[scancode] = bname
            self.lendedbooks[(scancode, bname)] = 'None'
            print('The book was sucessfully added to the store!!')
            Library.update_total_books(self)
                
    def discard(self):
        '''Deletes any book from the store not required'''
        scancode = list()
        bname = list()
        for i , idx in enumerate(self.listofbooks):
            scancode.append(idx)
            bname.append(self.listofbooks[idx])
        df = pd.DataFrame({'qr_code': scancode, 'Book_name':bname})
        df.index.name = 'Sl No'
        print(f'List of books available:\n  {df}')
        sl_no = int(input('Enter the SL No. for the book you want to delete from library: '))
        f= df.iloc[sl_no]
        self.lendedbooks.pop((f.values[0], f.values[1]))
        df.drop(sl_no, inplace = True)
        df.reset_index(inplace = True)
        df.drop('Sl No', axis = 1, inplace = True)
        df.index.name = 'Sl No'
        print(f'Updated book list:\n {df}')
        df.set_index('qr_code', inplace = True)
        m = df.to_dict()
        new_dic = {}
        for x in m.values():
            new_dic.update(x)
        self.listofbooks = new_dic
        Library.update_total_books(self)

    
def main():

    while True:

        ip = input('Enter the option no:\n1.Display the total books in the library store\n2.Borrow/Issue the book\n3.Submit/Return the book \n4.Add new book entries \n5.Delete any book from store\n')
        d = {'1': a.display, '2': a.borrow, '3': a.submit, '4': a.addbooks, '5':a.discard}

        d.get(ip, lambda : 'Enter valid input')()
        if ip  not in d.keys():
            print("Invalid input! Please try again!! ")
        ipx = input("Press c to continue or q to quit: ").lower()
        if ipx == 'q':
            try:
                sys.exit(0)
            except SystemExit as e:
                print('Program quitted')
                break
        elif ipx == 'c':
            continue
         
        else:
            print('Program Terminated! Enter Valid input')
            break
        
if __name__ == '__main__':
                         
    listofbooks = {'ISBN10':  'Harry-Potter' ,  'ISN12':'Kim-Jong', 'ISBN345':'Kite-Runner',  'ISBN89': 'Kite-Runner'}
    a = Library(listofbooks , 'Meghaswon')
    main()