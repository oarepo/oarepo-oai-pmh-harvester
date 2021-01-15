from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError


def oai_records_to_oai_identifiers():
    engine = create_engine('postgresql+psycopg2://oarepo:oarepo@localhost/oarepo')
    with engine.connect() as connection:
        result = connection.execute("select * from oarepo_oai_record")
        for row in result:
            id_ = row["id"]
            oai_id = row["oai_identifier"]
            connection.execute(f"""INSERT INTO oarepo_oai_identifiers (oai_record_id, 
            oai_identifier)
            VALUES ('{id_}', '{oai_id}');""")
            print(oai_id)


def records_to_oai_identifiers():
    engine = create_engine('postgresql+psycopg2://oarepo:oarepo@localhost/oarepo')
    with engine.connect() as connection:
        result = connection.execute("select * from records_metadata")
        for row in result:
            id_ = row["id"]
            json_ = row["json"]
            oai_id = json_.get('recordIdentifiers', {}).get('originalRecordOAI')
            if oai_id:
                try:
                    connection.execute(f"""INSERT INTO oarepo_oai_identifiers (oai_record_id, 
                    oai_identifier)
                    VALUES ('{id_}', '{oai_id}');""")
                    print(oai_id)
                except IntegrityError:
                    pass


if __name__ == '__main__':
    oai_records_to_oai_identifiers()
    records_to_oai_identifiers()
