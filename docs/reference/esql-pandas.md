---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/esql-pandas.html
---

# ES|QL and Pandas [esql-pandas]

The [Elasticsearch Query Language (ES|QL)](docs-content://explore-analyze/query-filter/languages/esql.md) provides a powerful way to filter, transform, and analyze data stored in {{es}}. Designed to be easy to learn and use, it is a perfect fit for data scientists familiar with Pandas and other dataframe-based libraries. ES|QL queries produce tables with named columns, which is the definition of dataframes.

This page shows you an example of using ES|QL and Pandas together to work with dataframes.


## Import data [import-data]

Use the [`employees` sample data](https://github.com/elastic/elasticsearch/blob/main/x-pack/plugin/esql/qa/testFixtures/src/main/resources/employees.csv) and [mapping](https://github.com/elastic/elasticsearch/blob/main/x-pack/plugin/esql/qa/testFixtures/src/main/resources/mapping-default.json). The easiest way to load this dataset is to run [two Elasticsearch API requests](https://gist.github.com/pquentin/7cf29a5932cf52b293699dd994b1a276) in the Kibana Console.

::::{dropdown} Index mapping request
```console
PUT employees
{
  "mappings": {
    "properties": {
      "avg_worked_seconds": {
        "type": "long"
      },
      "birth_date": {
        "type": "date"
      },
      "emp_no": {
        "type": "integer"
      },
      "first_name": {
        "type": "keyword"
      },
      "gender": {
        "type": "keyword"
      },
      "height": {
        "type": "double",
        "fields": {
          "float": {
            "type": "float"
          },
          "half_float": {
            "type": "half_float"
          },
          "scaled_float": {
            "type": "scaled_float",
            "scaling_factor": 100
          }
        }
      },
      "hire_date": {
        "type": "date"
      },
      "is_rehired": {
        "type": "boolean"
      },
      "job_positions": {
        "type": "keyword"
      },
      "languages": {
        "type": "integer",
        "fields": {
          "byte": {
            "type": "byte"
          },
          "long": {
            "type": "long"
          },
          "short": {
            "type": "short"
          }
        }
      },
      "last_name": {
        "type": "keyword"
      },
      "salary": {
        "type": "integer"
      },
      "salary_change": {
        "type": "double",
        "fields": {
          "int": {
            "type": "integer"
          },
          "keyword": {
            "type": "keyword"
          },
          "long": {
            "type": "long"
          }
        }
      },
      "still_hired": {
        "type": "boolean"
      }
    }
  }
}
```

::::


::::{dropdown} Bulk request to ingest data
```console
PUT employees/_bulk
{ "index": {}}
{"birth_date":"1953-09-02T00:00:00Z","emp_no":"10001","first_name":"Georgi","gender":"M","hire_date":"1986-06-26T00:00:00Z","languages":"2","last_name":"Facello","salary":"57305","height":"2.03","still_hired":"true","avg_worked_seconds":"268728049","job_positions":["Senior Python Developer","Accountant"],"is_rehired":["false","true"],"salary_change":"1.19"}
{ "index": {}}
{"birth_date":"1964-06-02T00:00:00Z","emp_no":"10002","first_name":"Bezalel","gender":"F","hire_date":"1985-11-21T00:00:00Z","languages":"5","last_name":"Simmel","salary":"56371","height":"2.08","still_hired":"true","avg_worked_seconds":"328922887","job_positions":"Senior Team Lead","is_rehired":["false","false"],"salary_change":["-7.23","11.17"]}
{ "index": {}}
{"birth_date":"1959-12-03T00:00:00Z","emp_no":"10003","first_name":"Parto","gender":"M","hire_date":"1986-08-28T00:00:00Z","languages":"4","last_name":"Bamford","salary":"61805","height":"1.83","still_hired":"false","avg_worked_seconds":"200296405","salary_change":["14.68","12.82"]}
{ "index": {}}
{"birth_date":"1954-05-01T00:00:00Z","emp_no":"10004","first_name":"Chirstian","gender":"M","hire_date":"1986-12-01T00:00:00Z","languages":"5","last_name":"Koblick","salary":"36174","height":"1.78","still_hired":"true","avg_worked_seconds":"311267831","job_positions":["Reporting Analyst","Tech Lead","Head Human Resources","Support Engineer"],"is_rehired":"true","salary_change":["3.65","-0.35","1.13","13.48"]}
{ "index": {}}
{"birth_date":"1955-01-21T00:00:00Z","emp_no":"10005","first_name":"Kyoichi","gender":"M","hire_date":"1989-09-12T00:00:00Z","languages":"1","last_name":"Maliniak","salary":"63528","height":"2.05","still_hired":"true","avg_worked_seconds":"244294991","is_rehired":["false","false","false","true"],"salary_change":["-2.14","13.07"]}
{ "index": {}}
{"birth_date":"1953-04-20T00:00:00Z","emp_no":"10006","first_name":"Anneke","gender":"F","hire_date":"1989-06-02T00:00:00Z","languages":"3","last_name":"Preusig","salary":"60335","height":"1.56","still_hired":"false","avg_worked_seconds":"372957040","job_positions":["Tech Lead","Principal Support Engineer","Senior Team Lead"],"salary_change":"-3.90"}
{ "index": {}}
{"birth_date":"1957-05-23T00:00:00Z","emp_no":"10007","first_name":"Tzvetan","gender":"F","hire_date":"1989-02-10T00:00:00Z","languages":"4","last_name":"Zielinski","salary":"74572","height":"1.70","still_hired":"true","avg_worked_seconds":"393084805","is_rehired":["true","false","true","false"],"salary_change":["-7.06","1.99","0.57"]}
{ "index": {}}
{"birth_date":"1958-02-19T00:00:00Z","emp_no":"10008","first_name":"Saniya","gender":"M","hire_date":"1994-09-15T00:00:00Z","languages":"2","last_name":"Kalloufi","salary":"43906","height":"2.10","still_hired":"true","avg_worked_seconds":"283074758","job_positions":["Senior Python Developer","Junior Developer","Purchase Manager","Internship"],"is_rehired":["true","false"],"salary_change":["12.68","3.54","0.75","-2.92"]}
{ "index": {}}
{"birth_date":"1952-04-19T00:00:00Z","emp_no":"10009","first_name":"Sumant","gender":"F","hire_date":"1985-02-18T00:00:00Z","languages":"1","last_name":"Peac","salary":"66174","height":"1.85","still_hired":"false","avg_worked_seconds":"236805489","job_positions":["Senior Python Developer","Internship"]}
{ "index": {}}
{"birth_date":"1963-06-01T00:00:00Z","emp_no":"10010","first_name":"Duangkaew","hire_date":"1989-08-24T00:00:00Z","languages":"4","last_name":"Piveteau","salary":"45797","height":"1.70","still_hired":"false","avg_worked_seconds":"315236372","job_positions":["Architect","Reporting Analyst","Tech Lead","Purchase Manager"],"is_rehired":["true","true","false","false"],"salary_change":["5.05","-6.77","4.69","12.15"]}
{ "index": {}}
{"birth_date":"1953-11-07T00:00:00Z","emp_no":"10011","first_name":"Mary","hire_date":"1990-01-22T00:00:00Z","languages":"5","last_name":"Sluis","salary":"31120","height":"1.50","still_hired":"true","avg_worked_seconds":"239615525","job_positions":["Architect","Reporting Analyst","Tech Lead","Senior Team Lead"],"is_rehired":["true","true"],"salary_change":["10.35","-7.82","8.73","3.48"]}
{ "index": {}}
{"birth_date":"1960-10-04T00:00:00Z","emp_no":"10012","first_name":"Patricio","hire_date":"1992-12-18T00:00:00Z","languages":"5","last_name":"Bridgland","salary":"48942","height":"1.97","still_hired":"false","avg_worked_seconds":"365510850","job_positions":["Head Human Resources","Accountant"],"is_rehired":["false","true","true","false"],"salary_change":"0.04"}
{ "index": {}}
{"birth_date":"1963-06-07T00:00:00Z","emp_no":"10013","first_name":"Eberhardt","hire_date":"1985-10-20T00:00:00Z","languages":"1","last_name":"Terkki","salary":"48735","height":"1.94","still_hired":"true","avg_worked_seconds":"253864340","job_positions":"Reporting Analyst","is_rehired":["true","true"]}
{ "index": {}}
{"birth_date":"1956-02-12T00:00:00Z","emp_no":"10014","first_name":"Berni","hire_date":"1987-03-11T00:00:00Z","languages":"5","last_name":"Genin","salary":"37137","height":"1.99","still_hired":"false","avg_worked_seconds":"225049139","job_positions":["Reporting Analyst","Data Scientist","Head Human Resources"],"salary_change":["-1.89","9.07"]}
{ "index": {}}
{"birth_date":"1959-08-19T00:00:00Z","emp_no":"10015","first_name":"Guoxiang","hire_date":"1987-07-02T00:00:00Z","languages":"5","last_name":"Nooteboom","salary":"25324","height":"1.66","still_hired":"true","avg_worked_seconds":"390266432","job_positions":["Principal Support Engineer","Junior Developer","Head Human Resources","Support Engineer"],"is_rehired":["true","false","false","false"],"salary_change":["14.25","12.40"]}
{ "index": {}}
{"birth_date":"1961-05-02T00:00:00Z","emp_no":"10016","first_name":"Kazuhito","hire_date":"1995-01-27T00:00:00Z","languages":"2","last_name":"Cappelletti","salary":"61358","height":"1.54","still_hired":"false","avg_worked_seconds":"253029411","job_positions":["Reporting Analyst","Python Developer","Accountant","Purchase Manager"],"is_rehired":["false","false"],"salary_change":["-5.18","7.69"]}
{ "index": {}}
{"birth_date":"1958-07-06T00:00:00Z","emp_no":"10017","first_name":"Cristinel","hire_date":"1993-08-03T00:00:00Z","languages":"2","last_name":"Bouloucos","salary":"58715","height":"1.74","still_hired":"false","avg_worked_seconds":"236703986","job_positions":["Data Scientist","Head Human Resources","Purchase Manager"],"is_rehired":["true","false","true","true"],"salary_change":"-6.33"}
{ "index": {}}
{"birth_date":"1954-06-19T00:00:00Z","emp_no":"10018","first_name":"Kazuhide","hire_date":"1987-04-03T00:00:00Z","languages":"2","last_name":"Peha","salary":"56760","height":"1.97","still_hired":"false","avg_worked_seconds":"309604079","job_positions":"Junior Developer","is_rehired":["false","false","true","true"],"salary_change":["-1.64","11.51","-5.32"]}
{ "index": {}}
{"birth_date":"1953-01-23T00:00:00Z","emp_no":"10019","first_name":"Lillian","hire_date":"1999-04-30T00:00:00Z","languages":"1","last_name":"Haddadi","salary":"73717","height":"2.06","still_hired":"false","avg_worked_seconds":"342855721","job_positions":"Purchase Manager","is_rehired":["false","false"],"salary_change":["-6.84","8.42","-7.26"]}
{ "index": {}}
{"birth_date":"1952-12-24T00:00:00Z","emp_no":"10020","first_name":"Mayuko","gender":"M","hire_date":"1991-01-26T00:00:00Z","last_name":"Warwick","salary":"40031","height":"1.41","still_hired":"false","avg_worked_seconds":"373309605","job_positions":"Tech Lead","is_rehired":["true","true","false"],"salary_change":"-5.81"}
{ "index": {}}
{"birth_date":"1960-02-20T00:00:00Z","emp_no":"10021","first_name":"Ramzi","gender":"M","hire_date":"1988-02-10T00:00:00Z","last_name":"Erde","salary":"60408","height":"1.47","still_hired":"false","avg_worked_seconds":"287654610","job_positions":"Support Engineer","is_rehired":"true"}
{ "index": {}}
{"birth_date":"1952-07-08T00:00:00Z","emp_no":"10022","first_name":"Shahaf","gender":"M","hire_date":"1995-08-22T00:00:00Z","last_name":"Famili","salary":"48233","height":"1.82","still_hired":"false","avg_worked_seconds":"233521306","job_positions":["Reporting Analyst","Data Scientist","Python Developer","Internship"],"is_rehired":["true","false"],"salary_change":["12.09","2.85"]}
{ "index": {}}
{"birth_date":"1953-09-29T00:00:00Z","emp_no":"10023","first_name":"Bojan","gender":"F","hire_date":"1989-12-17T00:00:00Z","last_name":"Montemayor","salary":"47896","height":"1.75","still_hired":"true","avg_worked_seconds":"330870342","job_positions":["Accountant","Support Engineer","Purchase Manager"],"is_rehired":["true","true","false"],"salary_change":["14.63","0.80"]}
{ "index": {}}
{"birth_date":"1958-09-05T00:00:00Z","emp_no":"10024","first_name":"Suzette","gender":"F","hire_date":"1997-05-19T00:00:00Z","last_name":"Pettey","salary":"64675","height":"2.08","still_hired":"true","avg_worked_seconds":"367717671","job_positions":"Junior Developer","is_rehired":["true","true","true","true"]}
{ "index": {}}
{"birth_date":"1958-10-31T00:00:00Z","emp_no":"10025","first_name":"Prasadram","gender":"M","hire_date":"1987-08-17T00:00:00Z","last_name":"Heyers","salary":"47411","height":"1.87","still_hired":"false","avg_worked_seconds":"371270797","job_positions":"Accountant","is_rehired":["true","false"],"salary_change":["-4.33","-2.90","12.06","-3.46"]}
{ "index": {}}
{"birth_date":"1953-04-03T00:00:00Z","emp_no":"10026","first_name":"Yongqiao","gender":"M","hire_date":"1995-03-20T00:00:00Z","last_name":"Berztiss","salary":"28336","height":"2.10","still_hired":"true","avg_worked_seconds":"359208133","job_positions":"Reporting Analyst","is_rehired":["false","true"],"salary_change":["-7.37","10.62","11.20"]}
{ "index": {}}
{"birth_date":"1962-07-10T00:00:00Z","emp_no":"10027","first_name":"Divier","gender":"F","hire_date":"1989-07-07T00:00:00Z","last_name":"Reistad","salary":"73851","height":"1.53","still_hired":"false","avg_worked_seconds":"374037782","job_positions":"Senior Python Developer","is_rehired":"false"}
{ "index": {}}
{"birth_date":"1963-11-26T00:00:00Z","emp_no":"10028","first_name":"Domenick","gender":"M","hire_date":"1991-10-22T00:00:00Z","last_name":"Tempesti","salary":"39356","height":"2.07","still_hired":"true","avg_worked_seconds":"226435054","job_positions":["Tech Lead","Python Developer","Accountant","Internship"],"is_rehired":["true","false","false","true"]}
{ "index": {}}
{"birth_date":"1956-12-13T00:00:00Z","emp_no":"10029","first_name":"Otmar","gender":"M","hire_date":"1985-11-20T00:00:00Z","last_name":"Herbst","salary":"74999","height":"1.99","still_hired":"false","avg_worked_seconds":"257694181","job_positions":["Senior Python Developer","Data Scientist","Principal Support Engineer"],"is_rehired":"true","salary_change":["-0.32","-1.90","-8.19"]}
{ "index": {}}
{"birth_date":"1958-07-14T00:00:00Z","emp_no":"10030","gender":"M","hire_date":"1994-02-17T00:00:00Z","languages":"3","last_name":"Demeyer","salary":"67492","height":"1.92","still_hired":"false","avg_worked_seconds":"394597613","job_positions":["Tech Lead","Data Scientist","Senior Team Lead"],"is_rehired":["true","false","false"],"salary_change":"-0.40"}
{ "index": {}}
{"birth_date":"1959-01-27T00:00:00Z","emp_no":"10031","gender":"M","hire_date":"1991-09-01T00:00:00Z","languages":"4","last_name":"Joslin","salary":"37716","height":"1.68","still_hired":"false","avg_worked_seconds":"348545109","job_positions":["Architect","Senior Python Developer","Purchase Manager","Senior Team Lead"],"is_rehired":"false"}
{ "index": {}}
{"birth_date":"1960-08-09T00:00:00Z","emp_no":"10032","gender":"F","hire_date":"1990-06-20T00:00:00Z","languages":"3","last_name":"Reistad","salary":"62233","height":"2.10","still_hired":"false","avg_worked_seconds":"277622619","job_positions":["Architect","Senior Python Developer","Junior Developer","Purchase Manager"],"is_rehired":["false","false"],"salary_change":["9.32","-4.92"]}
{ "index": {}}
{"birth_date":"1956-11-14T00:00:00Z","emp_no":"10033","gender":"M","hire_date":"1987-03-18T00:00:00Z","languages":"1","last_name":"Merlo","salary":"70011","height":"1.63","still_hired":"false","avg_worked_seconds":"208374744","is_rehired":"true"}
{ "index": {}}
{"birth_date":"1962-12-29T00:00:00Z","emp_no":"10034","gender":"M","hire_date":"1988-09-21T00:00:00Z","languages":"1","last_name":"Swan","salary":"39878","height":"1.46","still_hired":"false","avg_worked_seconds":"214393176","job_positions":["Business Analyst","Data Scientist","Python Developer","Accountant"],"is_rehired":"false","salary_change":"-8.46"}
{ "index": {}}
{"birth_date":"1953-02-08T00:00:00Z","emp_no":"10035","gender":"M","hire_date":"1988-09-05T00:00:00Z","languages":"5","last_name":"Chappelet","salary":"25945","height":"1.81","still_hired":"false","avg_worked_seconds":"203838153","job_positions":["Senior Python Developer","Data Scientist"],"is_rehired":"false","salary_change":["-2.54","-6.58"]}
{ "index": {}}
{"birth_date":"1959-08-10T00:00:00Z","emp_no":"10036","gender":"M","hire_date":"1992-01-03T00:00:00Z","languages":"4","last_name":"Portugali","salary":"60781","height":"1.61","still_hired":"false","avg_worked_seconds":"305493131","job_positions":"Senior Python Developer","is_rehired":["true","false","false"]}
{ "index": {}}
{"birth_date":"1963-07-22T00:00:00Z","emp_no":"10037","gender":"M","hire_date":"1990-12-05T00:00:00Z","languages":"2","last_name":"Makrucki","salary":"37691","height":"2.00","still_hired":"true","avg_worked_seconds":"359217000","job_positions":["Senior Python Developer","Tech Lead","Accountant"],"is_rehired":"false","salary_change":"-7.08"}
{ "index": {}}
{"birth_date":"1960-07-20T00:00:00Z","emp_no":"10038","gender":"M","hire_date":"1989-09-20T00:00:00Z","languages":"4","last_name":"Lortz","salary":"35222","height":"1.53","still_hired":"true","avg_worked_seconds":"314036411","job_positions":["Senior Python Developer","Python Developer","Support Engineer"]}
{ "index": {}}
{"birth_date":"1959-10-01T00:00:00Z","emp_no":"10039","gender":"M","hire_date":"1988-01-19T00:00:00Z","languages":"2","last_name":"Brender","salary":"36051","height":"1.55","still_hired":"false","avg_worked_seconds":"243221262","job_positions":["Business Analyst","Python Developer","Principal Support Engineer"],"is_rehired":["true","true"],"salary_change":"-6.90"}
{ "index": {}}
{"emp_no":"10040","first_name":"Weiyi","gender":"F","hire_date":"1993-02-14T00:00:00Z","languages":"4","last_name":"Meriste","salary":"37112","height":"1.90","still_hired":"false","avg_worked_seconds":"244478622","job_positions":"Principal Support Engineer","is_rehired":["true","false","true","true"],"salary_change":["6.97","14.74","-8.94","1.92"]}
{ "index": {}}
{"emp_no":"10041","first_name":"Uri","gender":"F","hire_date":"1989-11-12T00:00:00Z","languages":"1","last_name":"Lenart","salary":"56415","height":"1.75","still_hired":"false","avg_worked_seconds":"287789442","job_positions":["Data Scientist","Head Human Resources","Internship","Senior Team Lead"],"salary_change":["9.21","0.05","7.29","-2.94"]}
{ "index": {}}
{"emp_no":"10042","first_name":"Magy","gender":"F","hire_date":"1993-03-21T00:00:00Z","languages":"3","last_name":"Stamatiou","salary":"30404","height":"1.44","still_hired":"true","avg_worked_seconds":"246355863","job_positions":["Architect","Business Analyst","Junior Developer","Internship"],"salary_change":["-9.28","9.42"]}
{ "index": {}}
{"emp_no":"10043","first_name":"Yishay","gender":"M","hire_date":"1990-10-20T00:00:00Z","languages":"1","last_name":"Tzvieli","salary":"34341","height":"1.52","still_hired":"true","avg_worked_seconds":"287222180","job_positions":["Data Scientist","Python Developer","Support Engineer"],"is_rehired":["false","true","true"],"salary_change":["-5.17","4.62","7.42"]}
{ "index": {}}
{"emp_no":"10044","first_name":"Mingsen","gender":"F","hire_date":"1994-05-21T00:00:00Z","languages":"1","last_name":"Casley","salary":"39728","height":"2.06","still_hired":"false","avg_worked_seconds":"387408356","job_positions":["Tech Lead","Principal Support Engineer","Accountant","Support Engineer"],"is_rehired":["true","true"],"salary_change":"8.09"}
{ "index": {}}
{"emp_no":"10045","first_name":"Moss","gender":"M","hire_date":"1989-09-02T00:00:00Z","languages":"3","last_name":"Shanbhogue","salary":"74970","height":"1.70","still_hired":"false","avg_worked_seconds":"371418933","job_positions":["Principal Support Engineer","Junior Developer","Accountant","Purchase Manager"],"is_rehired":["true","false"]}
{ "index": {}}
{"emp_no":"10046","first_name":"Lucien","gender":"M","hire_date":"1992-06-20T00:00:00Z","languages":"4","last_name":"Rosenbaum","salary":"50064","height":"1.52","still_hired":"true","avg_worked_seconds":"302353405","job_positions":["Principal Support Engineer","Junior Developer","Head Human Resources","Internship"],"is_rehired":["true","true","false","true"],"salary_change":"2.39"}
{ "index": {}}
{"emp_no":"10047","first_name":"Zvonko","gender":"M","hire_date":"1989-03-31T00:00:00Z","languages":"4","last_name":"Nyanchama","salary":"42716","height":"1.52","still_hired":"true","avg_worked_seconds":"306369346","job_positions":["Architect","Data Scientist","Principal Support Engineer","Senior Team Lead"],"is_rehired":"true","salary_change":["-6.36","12.12"]}
{ "index": {}}
{"emp_no":"10048","first_name":"Florian","gender":"M","hire_date":"1985-02-24T00:00:00Z","languages":"3","last_name":"Syrotiuk","salary":"26436","height":"2.00","still_hired":"false","avg_worked_seconds":"248451647","job_positions":"Internship","is_rehired":["true","true"]}
{ "index": {}}
{"emp_no":"10049","first_name":"Basil","gender":"F","hire_date":"1992-05-04T00:00:00Z","languages":"5","last_name":"Tramer","salary":"37853","height":"1.52","still_hired":"true","avg_worked_seconds":"320725709","job_positions":["Senior Python Developer","Business Analyst"],"salary_change":"-1.05"}
{ "index": {}}
{"birth_date":"1958-05-21T00:00:00Z","emp_no":"10050","first_name":"Yinghua","gender":"M","hire_date":"1990-12-25T00:00:00Z","languages":"2","last_name":"Dredge","salary":"43026","height":"1.96","still_hired":"true","avg_worked_seconds":"242731798","job_positions":["Reporting Analyst","Junior Developer","Accountant","Support Engineer"],"is_rehired":"true","salary_change":["8.70","10.94"]}
{ "index": {}}
{"birth_date":"1953-07-28T00:00:00Z","emp_no":"10051","first_name":"Hidefumi","gender":"M","hire_date":"1992-10-15T00:00:00Z","languages":"3","last_name":"Caine","salary":"58121","height":"1.89","still_hired":"true","avg_worked_seconds":"374753122","job_positions":["Business Analyst","Accountant","Purchase Manager"]}
{ "index": {}}
{"birth_date":"1961-02-26T00:00:00Z","emp_no":"10052","first_name":"Heping","gender":"M","hire_date":"1988-05-21T00:00:00Z","languages":"1","last_name":"Nitsch","salary":"55360","height":"1.79","still_hired":"true","avg_worked_seconds":"299654717","is_rehired":["true","true","false"],"salary_change":["-0.55","-1.89","-4.22","-6.03"]}
{ "index": {}}
{"birth_date":"1954-09-13T00:00:00Z","emp_no":"10053","first_name":"Sanjiv","gender":"F","hire_date":"1986-02-04T00:00:00Z","languages":"3","last_name":"Zschoche","salary":"54462","height":"1.58","still_hired":"false","avg_worked_seconds":"368103911","job_positions":"Support Engineer","is_rehired":["true","false","true","false"],"salary_change":["-7.67","-3.25"]}
{ "index": {}}
{"birth_date":"1957-04-04T00:00:00Z","emp_no":"10054","first_name":"Mayumi","gender":"M","hire_date":"1995-03-13T00:00:00Z","languages":"4","last_name":"Schueller","salary":"65367","height":"1.82","still_hired":"false","avg_worked_seconds":"297441693","job_positions":"Principal Support Engineer","is_rehired":["false","false"]}
{ "index": {}}
{"birth_date":"1956-06-06T00:00:00Z","emp_no":"10055","first_name":"Georgy","gender":"M","hire_date":"1992-04-27T00:00:00Z","languages":"5","last_name":"Dredge","salary":"49281","height":"2.04","still_hired":"false","avg_worked_seconds":"283157844","job_positions":["Senior Python Developer","Head Human Resources","Internship","Support Engineer"],"is_rehired":["false","false","true"],"salary_change":["7.34","12.99","3.17"]}
{ "index": {}}
{"birth_date":"1961-09-01T00:00:00Z","emp_no":"10056","first_name":"Brendon","gender":"F","hire_date":"1990-02-01T00:00:00Z","languages":"2","last_name":"Bernini","salary":"33370","height":"1.57","still_hired":"true","avg_worked_seconds":"349086555","job_positions":"Senior Team Lead","is_rehired":["true","false","false"],"salary_change":["10.99","-5.17"]}
{ "index": {}}
{"birth_date":"1954-05-30T00:00:00Z","emp_no":"10057","first_name":"Ebbe","gender":"F","hire_date":"1992-01-15T00:00:00Z","languages":"4","last_name":"Callaway","salary":"27215","height":"1.59","still_hired":"true","avg_worked_seconds":"324356269","job_positions":["Python Developer","Head Human Resources"],"salary_change":["-6.73","-2.43","-5.27","1.03"]}
{ "index": {}}
{"birth_date":"1954-10-01T00:00:00Z","emp_no":"10058","first_name":"Berhard","gender":"M","hire_date":"1987-04-13T00:00:00Z","languages":"3","last_name":"McFarlin","salary":"38376","height":"1.83","still_hired":"false","avg_worked_seconds":"268378108","job_positions":"Principal Support Engineer","salary_change":"-4.89"}
{ "index": {}}
{"birth_date":"1953-09-19T00:00:00Z","emp_no":"10059","first_name":"Alejandro","gender":"F","hire_date":"1991-06-26T00:00:00Z","languages":"2","last_name":"McAlpine","salary":"44307","height":"1.48","still_hired":"false","avg_worked_seconds":"237368465","job_positions":["Architect","Principal Support Engineer","Purchase Manager","Senior Team Lead"],"is_rehired":"false","salary_change":["5.53","13.38","-4.69","6.27"]}
{ "index": {}}
{"birth_date":"1961-10-15T00:00:00Z","emp_no":"10060","first_name":"Breannda","gender":"M","hire_date":"1987-11-02T00:00:00Z","languages":"2","last_name":"Billingsley","salary":"29175","height":"1.42","still_hired":"true","avg_worked_seconds":"341158890","job_positions":["Business Analyst","Data Scientist","Senior Team Lead"],"is_rehired":["false","false","true","false"],"salary_change":["-1.76","-0.85"]}
{ "index": {}}
{"birth_date":"1962-10-19T00:00:00Z","emp_no":"10061","first_name":"Tse","gender":"M","hire_date":"1985-09-17T00:00:00Z","languages":"1","last_name":"Herber","salary":"49095","height":"1.45","still_hired":"false","avg_worked_seconds":"327550310","job_positions":["Purchase Manager","Senior Team Lead"],"is_rehired":["false","true"],"salary_change":["14.39","-2.58","-0.95"]}
{ "index": {}}
{"birth_date":"1961-11-02T00:00:00Z","emp_no":"10062","first_name":"Anoosh","gender":"M","hire_date":"1991-08-30T00:00:00Z","languages":"3","last_name":"Peyn","salary":"65030","height":"1.70","still_hired":"false","avg_worked_seconds":"203989706","job_positions":["Python Developer","Senior Team Lead"],"is_rehired":["false","true","true"],"salary_change":"-1.17"}
{ "index": {}}
{"birth_date":"1952-08-06T00:00:00Z","emp_no":"10063","first_name":"Gino","gender":"F","hire_date":"1989-04-08T00:00:00Z","languages":"3","last_name":"Leonhardt","salary":"52121","height":"1.78","still_hired":"true","avg_worked_seconds":"214068302","is_rehired":"true"}
{ "index": {}}
{"birth_date":"1959-04-07T00:00:00Z","emp_no":"10064","first_name":"Udi","gender":"M","hire_date":"1985-11-20T00:00:00Z","languages":"5","last_name":"Jansch","salary":"33956","height":"1.93","still_hired":"false","avg_worked_seconds":"307364077","job_positions":"Purchase Manager","is_rehired":["false","false","true","false"],"salary_change":["-8.66","-2.52"]}
{ "index": {}}
{"birth_date":"1963-04-14T00:00:00Z","emp_no":"10065","first_name":"Satosi","gender":"M","hire_date":"1988-05-18T00:00:00Z","languages":"2","last_name":"Awdeh","salary":"50249","height":"1.59","still_hired":"false","avg_worked_seconds":"372660279","job_positions":["Business Analyst","Data Scientist","Principal Support Engineer"],"is_rehired":["false","true"],"salary_change":["-1.47","14.44","-9.81"]}
{ "index": {}}
{"birth_date":"1952-11-13T00:00:00Z","emp_no":"10066","first_name":"Kwee","gender":"M","hire_date":"1986-02-26T00:00:00Z","languages":"5","last_name":"Schusler","salary":"31897","height":"2.10","still_hired":"true","avg_worked_seconds":"360906451","job_positions":["Senior Python Developer","Data Scientist","Accountant","Internship"],"is_rehired":["true","true","true"],"salary_change":"5.94"}
{ "index": {}}
{"birth_date":"1953-01-07T00:00:00Z","emp_no":"10067","first_name":"Claudi","gender":"M","hire_date":"1987-03-04T00:00:00Z","languages":"2","last_name":"Stavenow","salary":"52044","height":"1.77","still_hired":"true","avg_worked_seconds":"347664141","job_positions":["Tech Lead","Principal Support Engineer"],"is_rehired":["false","false"],"salary_change":["8.72","4.44"]}
{ "index": {}}
{"birth_date":"1962-11-26T00:00:00Z","emp_no":"10068","first_name":"Charlene","gender":"M","hire_date":"1987-08-07T00:00:00Z","languages":"3","last_name":"Brattka","salary":"28941","height":"1.58","still_hired":"true","avg_worked_seconds":"233999584","job_positions":"Architect","is_rehired":"true","salary_change":["3.43","-5.61","-5.29"]}
{ "index": {}}
{"birth_date":"1960-09-06T00:00:00Z","emp_no":"10069","first_name":"Margareta","gender":"F","hire_date":"1989-11-05T00:00:00Z","languages":"5","last_name":"Bierman","salary":"41933","height":"1.77","still_hired":"true","avg_worked_seconds":"366512352","job_positions":["Business Analyst","Junior Developer","Purchase Manager","Support Engineer"],"is_rehired":"false","salary_change":["-3.34","-6.33","6.23","-0.31"]}
{ "index": {}}
{"birth_date":"1955-08-20T00:00:00Z","emp_no":"10070","first_name":"Reuven","gender":"M","hire_date":"1985-10-14T00:00:00Z","languages":"3","last_name":"Garigliano","salary":"54329","height":"1.77","still_hired":"true","avg_worked_seconds":"347188604","is_rehired":["true","true","true"],"salary_change":"-5.90"}
{ "index": {}}
{"birth_date":"1958-01-21T00:00:00Z","emp_no":"10071","first_name":"Hisao","gender":"M","hire_date":"1987-10-01T00:00:00Z","languages":"2","last_name":"Lipner","salary":"40612","height":"2.07","still_hired":"false","avg_worked_seconds":"306671693","job_positions":["Business Analyst","Reporting Analyst","Senior Team Lead"],"is_rehired":["false","false","false"],"salary_change":"-2.69"}
{ "index": {}}
{"birth_date":"1952-05-15T00:00:00Z","emp_no":"10072","first_name":"Hironoby","gender":"F","hire_date":"1988-07-21T00:00:00Z","languages":"5","last_name":"Sidou","salary":"54518","height":"1.82","still_hired":"true","avg_worked_seconds":"209506065","job_positions":["Architect","Tech Lead","Python Developer","Senior Team Lead"],"is_rehired":["false","false","true","false"],"salary_change":["11.21","-2.30","2.22","-5.44"]}
{ "index": {}}
{"birth_date":"1954-02-23T00:00:00Z","emp_no":"10073","first_name":"Shir","gender":"M","hire_date":"1991-12-01T00:00:00Z","languages":"4","last_name":"McClurg","salary":"32568","height":"1.66","still_hired":"false","avg_worked_seconds":"314930367","job_positions":["Principal Support Engineer","Python Developer","Junior Developer","Purchase Manager"],"is_rehired":["true","false"],"salary_change":"-5.67"}
{ "index": {}}
{"birth_date":"1955-08-28T00:00:00Z","emp_no":"10074","first_name":"Mokhtar","gender":"F","hire_date":"1990-08-13T00:00:00Z","languages":"5","last_name":"Bernatsky","salary":"38992","height":"1.64","still_hired":"true","avg_worked_seconds":"382397583","job_positions":["Senior Python Developer","Python Developer"],"is_rehired":["true","false","false","true"],"salary_change":["6.70","1.98","-5.64","2.96"]}
{ "index": {}}
{"birth_date":"1960-03-09T00:00:00Z","emp_no":"10075","first_name":"Gao","gender":"F","hire_date":"1987-03-19T00:00:00Z","languages":"5","last_name":"Dolinsky","salary":"51956","height":"1.94","still_hired":"false","avg_worked_seconds":"370238919","job_positions":"Purchase Manager","is_rehired":"true","salary_change":["9.63","-3.29","8.42"]}
{ "index": {}}
{"birth_date":"1952-06-13T00:00:00Z","emp_no":"10076","first_name":"Erez","gender":"F","hire_date":"1985-07-09T00:00:00Z","languages":"3","last_name":"Ritzmann","salary":"62405","height":"1.83","still_hired":"false","avg_worked_seconds":"376240317","job_positions":["Architect","Senior Python Developer"],"is_rehired":"false","salary_change":["-6.90","-1.30","8.75"]}
{ "index": {}}
{"birth_date":"1964-04-18T00:00:00Z","emp_no":"10077","first_name":"Mona","gender":"M","hire_date":"1990-03-02T00:00:00Z","languages":"5","last_name":"Azuma","salary":"46595","height":"1.68","still_hired":"false","avg_worked_seconds":"351960222","job_positions":"Internship","salary_change":"-0.01"}
{ "index": {}}
{"birth_date":"1959-12-25T00:00:00Z","emp_no":"10078","first_name":"Danel","gender":"F","hire_date":"1987-05-26T00:00:00Z","languages":"2","last_name":"Mondadori","salary":"69904","height":"1.81","still_hired":"true","avg_worked_seconds":"377116038","job_positions":["Architect","Principal Support Engineer","Internship"],"is_rehired":"true","salary_change":["-7.88","9.98","12.52"]}
{ "index": {}}
{"birth_date":"1961-10-05T00:00:00Z","emp_no":"10079","first_name":"Kshitij","gender":"F","hire_date":"1986-03-27T00:00:00Z","languages":"2","last_name":"Gils","salary":"32263","height":"1.59","still_hired":"false","avg_worked_seconds":"320953330","is_rehired":"false","salary_change":"7.58"}
{ "index": {}}
{"birth_date":"1957-12-03T00:00:00Z","emp_no":"10080","first_name":"Premal","gender":"M","hire_date":"1985-11-19T00:00:00Z","languages":"5","last_name":"Baek","salary":"52833","height":"1.80","still_hired":"false","avg_worked_seconds":"239266137","job_positions":"Senior Python Developer","salary_change":["-4.35","7.36","5.56"]}
{ "index": {}}
{"birth_date":"1960-12-17T00:00:00Z","emp_no":"10081","first_name":"Zhongwei","gender":"M","hire_date":"1986-10-30T00:00:00Z","languages":"2","last_name":"Rosen","salary":"50128","height":"1.44","still_hired":"true","avg_worked_seconds":"321375511","job_positions":["Accountant","Internship"],"is_rehired":["false","false","false"]}
{ "index": {}}
{"birth_date":"1963-09-09T00:00:00Z","emp_no":"10082","first_name":"Parviz","gender":"M","hire_date":"1990-01-03T00:00:00Z","languages":"4","last_name":"Lortz","salary":"49818","height":"1.61","still_hired":"false","avg_worked_seconds":"232522994","job_positions":"Principal Support Engineer","is_rehired":"false","salary_change":["1.19","-3.39"]}
{ "index": {}}
{"birth_date":"1959-07-23T00:00:00Z","emp_no":"10083","first_name":"Vishv","gender":"M","hire_date":"1987-03-31T00:00:00Z","languages":"1","last_name":"Zockler","salary":"39110","height":"1.42","still_hired":"false","avg_worked_seconds":"331236443","job_positions":"Head Human Resources"}
{ "index": {}}
{"birth_date":"1960-05-25T00:00:00Z","emp_no":"10084","first_name":"Tuval","gender":"M","hire_date":"1995-12-15T00:00:00Z","languages":"1","last_name":"Kalloufi","salary":"28035","height":"1.51","still_hired":"true","avg_worked_seconds":"359067056","job_positions":"Principal Support Engineer","is_rehired":"false"}
{ "index": {}}
{"birth_date":"1962-11-07T00:00:00Z","emp_no":"10085","first_name":"Kenroku","gender":"M","hire_date":"1994-04-09T00:00:00Z","languages":"5","last_name":"Malabarba","salary":"35742","height":"2.01","still_hired":"true","avg_worked_seconds":"353404008","job_positions":["Senior Python Developer","Business Analyst","Tech Lead","Accountant"],"salary_change":["11.67","6.75","8.40"]}
{ "index": {}}
{"birth_date":"1962-11-19T00:00:00Z","emp_no":"10086","first_name":"Somnath","gender":"M","hire_date":"1990-02-16T00:00:00Z","languages":"1","last_name":"Foote","salary":"68547","height":"1.74","still_hired":"true","avg_worked_seconds":"328580163","job_positions":"Senior Python Developer","is_rehired":["false","true"],"salary_change":"13.61"}
{ "index": {}}
{"birth_date":"1959-07-23T00:00:00Z","emp_no":"10087","first_name":"Xinglin","gender":"F","hire_date":"1986-09-08T00:00:00Z","languages":"5","last_name":"Eugenio","salary":"32272","height":"1.74","still_hired":"true","avg_worked_seconds":"305782871","job_positions":["Junior Developer","Internship"],"is_rehired":["false","false"],"salary_change":"-2.05"}
{ "index": {}}
{"birth_date":"1954-02-25T00:00:00Z","emp_no":"10088","first_name":"Jungsoon","gender":"F","hire_date":"1988-09-02T00:00:00Z","languages":"5","last_name":"Syrzycki","salary":"39638","height":"1.91","still_hired":"false","avg_worked_seconds":"330714423","job_positions":["Reporting Analyst","Business Analyst","Tech Lead"],"is_rehired":"true"}
{ "index": {}}
{"birth_date":"1963-03-21T00:00:00Z","emp_no":"10089","first_name":"Sudharsan","gender":"F","hire_date":"1986-08-12T00:00:00Z","languages":"4","last_name":"Flasterstein","salary":"43602","height":"1.57","still_hired":"true","avg_worked_seconds":"232951673","job_positions":["Junior Developer","Accountant"],"is_rehired":["true","false","false","false"]}
{ "index": {}}
{"birth_date":"1961-05-30T00:00:00Z","emp_no":"10090","first_name":"Kendra","gender":"M","hire_date":"1986-03-14T00:00:00Z","languages":"2","last_name":"Hofting","salary":"44956","height":"2.03","still_hired":"true","avg_worked_seconds":"212460105","is_rehired":["false","false","false","true"],"salary_change":["7.15","-1.85","3.60"]}
{ "index": {}}
{"birth_date":"1955-10-04T00:00:00Z","emp_no":"10091","first_name":"Amabile","gender":"M","hire_date":"1992-11-18T00:00:00Z","languages":"3","last_name":"Gomatam","salary":"38645","height":"2.09","still_hired":"true","avg_worked_seconds":"242582807","job_positions":["Reporting Analyst","Python Developer"],"is_rehired":["true","true","false","false"],"salary_change":["-9.23","7.50","5.85","5.19"]}
{ "index": {}}
{"birth_date":"1964-10-18T00:00:00Z","emp_no":"10092","first_name":"Valdiodio","gender":"F","hire_date":"1989-09-22T00:00:00Z","languages":"1","last_name":"Niizuma","salary":"25976","height":"1.75","still_hired":"false","avg_worked_seconds":"313407352","job_positions":["Junior Developer","Accountant"],"is_rehired":["false","false","true","true"],"salary_change":["8.78","0.39","-6.77","8.30"]}
{ "index": {}}
{"birth_date":"1964-06-11T00:00:00Z","emp_no":"10093","first_name":"Sailaja","gender":"M","hire_date":"1996-11-05T00:00:00Z","languages":"3","last_name":"Desikan","salary":"45656","height":"1.69","still_hired":"false","avg_worked_seconds":"315904921","job_positions":["Reporting Analyst","Tech Lead","Principal Support Engineer","Purchase Manager"],"salary_change":"-0.88"}
{ "index": {}}
{"birth_date":"1957-05-25T00:00:00Z","emp_no":"10094","first_name":"Arumugam","gender":"F","hire_date":"1987-04-18T00:00:00Z","languages":"5","last_name":"Ossenbruggen","salary":"66817","height":"2.10","still_hired":"false","avg_worked_seconds":"332920135","job_positions":["Senior Python Developer","Principal Support Engineer","Accountant"],"is_rehired":["true","false","true"],"salary_change":["2.22","7.92"]}
{ "index": {}}
{"birth_date":"1965-01-03T00:00:00Z","emp_no":"10095","first_name":"Hilari","gender":"M","hire_date":"1986-07-15T00:00:00Z","languages":"4","last_name":"Morton","salary":"37702","height":"1.55","still_hired":"false","avg_worked_seconds":"321850475","is_rehired":["true","true","false","false"],"salary_change":["-3.93","-6.66"]}
{ "index": {}}
{"birth_date":"1954-09-16T00:00:00Z","emp_no":"10096","first_name":"Jayson","gender":"M","hire_date":"1990-01-14T00:00:00Z","languages":"4","last_name":"Mandell","salary":"43889","height":"1.94","still_hired":"false","avg_worked_seconds":"204381503","job_positions":["Architect","Reporting Analyst"],"is_rehired":["false","false","false"]}
{ "index": {}}
{"birth_date":"1952-02-27T00:00:00Z","emp_no":"10097","first_name":"Remzi","gender":"M","hire_date":"1990-09-15T00:00:00Z","languages":"3","last_name":"Waschkowski","salary":"71165","height":"1.53","still_hired":"false","avg_worked_seconds":"206258084","job_positions":["Reporting Analyst","Tech Lead"],"is_rehired":["true","false"],"salary_change":"-1.12"}
{ "index": {}}
{"birth_date":"1961-09-23T00:00:00Z","emp_no":"10098","first_name":"Sreekrishna","gender":"F","hire_date":"1985-05-13T00:00:00Z","languages":"4","last_name":"Servieres","salary":"44817","height":"2.00","still_hired":"false","avg_worked_seconds":"272392146","job_positions":["Architect","Internship","Senior Team Lead"],"is_rehired":"false","salary_change":["-2.83","8.31","4.38"]}
{ "index": {}}
{"birth_date":"1956-05-25T00:00:00Z","emp_no":"10099","first_name":"Valter","gender":"F","hire_date":"1988-10-18T00:00:00Z","languages":"2","last_name":"Sullins","salary":"73578","height":"1.81","still_hired":"true","avg_worked_seconds":"377713748","is_rehired":["true","true"],"salary_change":["10.71","14.26","-8.78","-3.98"]}
{ "index": {}}
{"birth_date":"1953-04-21T00:00:00Z","emp_no":"10100","first_name":"Hironobu","gender":"F","hire_date":"1987-09-21T00:00:00Z","languages":"4","last_name":"Haraldson","salary":"68431","height":"1.77","still_hired":"true","avg_worked_seconds":"223910853","job_positions":"Purchase Manager","is_rehired":["false","true","true","false"],"salary_change":["13.97","-7.49"]}
```

::::



## Convert the dataset [convert-dataset-pandas-dataframe]

Use the ES|QL CSV import to convert the `employees` dataset to a Pandas dataframe object.

```python
from io import StringIO
from elasticsearch import Elasticsearch
import pandas as pd
client = Elasticsearch(
    "https://[host].elastic-cloud.com",
    api_key="...",
)
response = client.esql.query(
    query="FROM employees | LIMIT 500",
    format="csv",
)
df = pd.read_csv(StringIO(response.body))
print(df)
```

Even though the dataset contains only 100 records, a LIMIT of 500 is specified to suppress ES|QL warnings about potentially missing records. This prints the following dataframe:

```python
    avg_worked_seconds  ...  salary_change.long still_hired
0            268728049  ...                   1        True
1            328922887  ...            [-7, 11]        True
2            200296405  ...            [12, 14]       False
3            311267831  ...       [0, 1, 3, 13]        True
4            244294991  ...            [-2, 13]        True
..                 ...  ...                 ...         ...
95           204381503  ...                 NaN       False
96           206258084  ...                  -1       False
97           272392146  ...          [-2, 4, 8]       False
98           377713748  ...    [-8, -3, 10, 14]        True
99           223910853  ...            [-7, 13]        True
```

You can now analyze the data with Pandas or you can also continue transforming the data using ES|QL.


## Analyze the data with Pandas [analyze-data]

In the next example, the [STATS … BY](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-stats-by) command is utilized to count how many employees are speaking a given language. The results are sorted with the `languages` column using [SORT](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-sort):

```python
response = client.esql.query(
    query="""
    FROM employees
    | STATS count = COUNT(emp_no) BY languages
    | SORT languages
    | LIMIT 500
    """,
    format="csv",
)
df = pd.read_csv(
    StringIO(response.body),
    dtype={"count": "Int64", "languages": "Int64"},
)
print(df)
```

Note that the `dtype` parameter of `pd.read_csv()` is useful when the type inferred by Pandas is not enough. The code prints the following response:

```python
   count  languages
0     15          1
1     19          2
2     17          3
3     18          4
4     21          5
```


## Pass parameters to a query with ES|QL [passing-params]

Use the [built-in parameters support of the ES|QL REST API](docs-content://explore-analyze/query-filter/languages/esql-rest.md#esql-rest-params) to pass parameters to a query:

```python
response = client.esql.query(
    query="""
    FROM employees
    | STATS count = COUNT(emp_no) BY languages
    | WHERE languages >= (?)
    | SORT languages
    | LIMIT 500
    """,
    format="csv",
    params=[3],
)
df = pd.read_csv(
    StringIO(response.body),
    dtype={"count": "Int64", "languages": "Int64"},
)
print(df)
```

The code above outputs the following:

```python
   count  languages
0     17          3
1     18          4
2     21          5
```

If you want to learn more about ES|QL, refer to the [ES|QL documentation](docs-content://explore-analyze/query-filter/languages/esql.md). You can also check out this other [Python example using Boston Celtics data](https://github.com/elastic/elasticsearch-labs/blob/main/supporting-blog-content/Boston-Celtics-Demo/celtics-esql-demo.ipynb).

