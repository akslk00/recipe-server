from flask import request
from flask_restful import Resource
from mysql_connection import get_connection
from mysql.connector import Error

# resources 폴더 안에 만드는 파일에는
# API를 만들기 위한 클래스를 작성한다

# API를 만들기 위해서는 flask_restful 라이브러리의 
# Resource 클래스를 상속해서 만들어야한다

class RecipeListResource(Resource):

    #http Method 와 동일한 함수명으로 오버라이딩
    def post(self):
        
        # 1. 클라이언트가 보내준 데이터가 있으면 
        #    그 데이터를 먼저 받아준다
        data = request.get_json()

        print(data)

        # 2. 받아온 레시피데이터를 DB에 저장해야한다
        
        try:
            # 2.1 DB에 연결하는 코드
            connection = get_connection()

            # 2.2 쿼리문 만들기 - insert 쿼리문 만들기
            query ='''insert into recipe
                        (name, description,num_of_servings, cook_time, direction)
                        values
                        (%s,%s,%s,%s,%s);'''
            # 2.3 위의 쿼리에 매칭되는 변수를 처리해준다.
            #       단, 라이브러리특성상 튜플로 만들어야한다.
            record = (data['name'],data['description'],data['num_of_servings'],
                      data['cook_time'],data['direction'])
            
            # 2.4 커서를 가져온다.
            cursor = connection.cursor()

            # 2.5 위의 쿼리문을 커서로 실행한다
            cursor.execute(query,record)

            # 2.6 커밋해줘야 DB에 완전히 반영된다.
            connection.commit()

            # 2.7 자원해제
            cursor.close()
            connection.close()


        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            # 유저한데 알려줘야한다. => response 해준다
            return {"result":"fail","error":str(e)}, 500
        
        # 3. DB에 잘 저장되었으면
        #    클라이언트에게 응답해준다.
        #    보내줄 정보(json)과 http 상태코드를
        #    리턴한다.
        return {"result":"success"}, 200