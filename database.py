import pymongo

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['test3']
        self.users_col = self.db['users']
        # self.add_user('roee90','a5759631358c3e45f25b1fef4ea68643171b1f9a6d5a16c78b4c88de8220510ecacb7d78044f2fa6bc332071c78fd005299eeada5c0b615666d5d3dc6d041886','manager')
        # self.add_user('almog','dea0ce4e8a19ef148b3704779a2f00c704aafead8cd99aa51d1fdbc0d7d51a7f6175ae8b01d20a3259465041cb22f5e354108bbed59c7c9b015d49adf91632f0','manager')
        # self.show_all_users()
        # self.drop_all_database()

    def add_user(self, nickname, password, user_type):
        my_query = {'nickname' : nickname}
        if self.users_col.count_documents(my_query) > 0:
            return '1'
        else:
            user_to_add = {            
                'nickname' : nickname,
                'password' : password,
                'user_type': user_type
                }
            self.users_col.insert_one(user_to_add)
            return '0'

    def add_manager(self, nickname):
        my_query = {'nickname' : nickname}
        my_query_two = {'nickname' : nickname, 'user_type': 'manager'}
        if self.users_col.count_documents(my_query) == 0:
            return '1'
        elif self.users_col.count_documents(my_query_two) == 1:
            return '2'
        else:
            new_values = {"$set": { "user_type": "manager" }}
            self.users_col.update_one(my_query, new_values)
        return '0'

    def authenticate_user(self, nickname, password):
        my_query = {'nickname': nickname}
        if len(password) < 8:
            return 'Password is wrong'
        if self.users_col.count_documents(my_query) == 0:
            return 'User not existing'
        my_query = {'nickname': nickname, 'password': password}
        if self.users_col.count_documents(my_query) == 0:
            return 'Password is wrong'
        return 'succed'

    def check_manager(self, nickname):
        my_query = {'nickname': nickname, 'user_type' : 'manager'}
        if self.users_col.count_documents(my_query) == 0:
            return 'member'
        else:
            return 'manager'

    def show_all_managers(self):
        my_query = {'user_type' : 'manager'}
        x = self.users_col.find(my_query)
        return x

    def delete_user(self, nickname):
        my_query = {'nickname' : nickname}
        if self.users_col.count_documents(my_query) == 0:
            return '1'
        else:
            self.users_col.delete_one(my_query)
            return '0'

    def show_all_users(self):
        result = self.users_col.find({})
        for x in result:
            print(f'almog be like: {x}')

    def drop_all_database(self):
        myquery = {}
        self.users_col.delete_many(myquery)

almg = Database()