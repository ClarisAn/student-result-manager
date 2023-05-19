'''
Database Connector Class for Postgres
'''

import psycopg2
from psycopg2.extras import RealDictCursor
import time
import logging
import os

logging.basicConfig(level=logging.INFO)

user = os.environ['dbUserName']
password = os.environ['dbPwd']
host = os.environ['dbHost']
port = os.environ['dbPort']
database = os.environ['dbName']
LIMIT_RETRIES = 3


# Create the DB Class and self assign variables
class Database:
    def __init__(self, user, password, host, port, database, reconnect):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self._connection = None
        self._cursor = None
        self.reconnect = reconnect
        self.init()

    '''
    Function that setups up the DB connections and retries up failure for 3 times. 
    Note autocommit default value is True i.e. will execute and commit the SQL query upon default True.
    Raises an error after > 3 times of failing. Note the function will also sleep 1 sec between each retry.
    Note the reconnect variable is a boolean (only if user wants to allow retries)
    '''

    def connect(self, retry_counter=0):
        logging.info("ENTERING connect")
        if not self._connection:
            try:
                self._connection = psycopg2.connect(user=self.user, password=self.password, host=self.host,
                                                    port=self.port, database=self.database, connect_timeout=3, )
                retry_counter = 0
                self._connection.autocommit = True
                logging.info("PostgreSQL connection is set up")
                return self._connection
            except psycopg2.OperationalError as error:
                if not self.reconnect or retry_counter >= LIMIT_RETRIES:
                    raise error
                else:
                    retry_counter += 1
                    logging.error("got error {}. reconnecting {}".format(str(error).strip(), retry_counter))
                    time.sleep(1)
                    self.connect(retry_counter)
            except (Exception, psycopg2.Error) as error:
                raise error
        logging.info("EXITING connect")

    # Function to setup cursor responsible for sql query execution
    def cursor(self):
        logging.info("ENTERING cursor")
        if not self._cursor or self._cursor.closed:
            if not self._connection:
                self.connect()
            self._cursor = self._connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            return self._cursor
        logging.info("EXITING cursor")

    '''
    Function which executes the SQL queries. Also retries for 3 times and sleeps 1 sec after every failed retry.
    Error handling after all attempts have failed and returns error messages. Returns values from DB
    '''

    def execute_result(self, query, retry_counter=0):
        logging.info("ENTERING execute_result")
        try:
            # Log query about to be executed for trouble shooting

            logging.info("About to execute query: {}".format(query))
            self._cursor.execute(query)

            retry_counter = 0
        except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
            if retry_counter >= LIMIT_RETRIES:
                raise error
            else:
                retry_counter += 1
                logging.error("got error {}. retrying {}".format(str(error).strip(), retry_counter))
                time.sleep(1)
                self.reset()
                self.execute_result(query, retry_counter)
        except (Exception, psycopg2.Error) as error:
            raise error
        logging.info("EXITING execute_result")
        return self._cursor.fetchall()

    '''
       Function which executes the SQL queries. Also retries for 3 times and sleeps 1 sec after every failed retry.
       Error handling after all attempts have failed and returns error messages. Returns no results
    '''

    def execute(self, query, retry_counter=0):
        logging.info("ENTERING execute")
        try:
            # Log query about to be executed for trouble shooting

            logging.info("About to execute query: {}".format(query))
            self._cursor.execute(query)

            retry_counter = 0
        except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
            if retry_counter >= LIMIT_RETRIES:
                raise error
            else:
                retry_counter += 1
                logging.error("got error {}. retrying {}".format(str(error).strip(), retry_counter))
                time.sleep(1)
                self.reset()
                self.execute_result(query, retry_counter)
        except (Exception, psycopg2.Error) as error:
            raise error
        logging.info("EXITING execute")

    # Function that resets connections upon retry
    def reset(self):
        logging.info("ENTERING reset")
        self.close()
        self.connect()
        self.cursor()
        logging.info("EXITING reset")

    # Function that closed connection to DB when query has been executed
    def close(self):
        logging.info("ENTERING close")
        if self._connection:
            if self._cursor:
                self._cursor.close()
            self._connection.close()
            logging.info("PostgreSQL connection is closed")
        self._connection = None
        self._cursor = None
        logging.info("EXITING close")

    # Self initializes functions in class
    def init(self):
        self.connect()
        self.cursor()
