"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}




# const { CloudantV1 } = require('@ibm-cloud/cloudant');
# const { IamAuthenticator } = require('ibm-cloud-sdk-core');

# function main(params) {
#         secret ={
#         "COUCH_URL": "https://ec96a461-e711-4471-8075-8e077c690cbb-bluemix.cloudantnosqldb.appdomain.cloud",
#         "IAM_API_KEY":"jUh8BbgAAd-qRBUBCHe0iHc6vxF6jKMK4pzEiqTQgCpF",
#         "COUCH_USERNAME":"ec96a461-e711-4471-8075-8e077c690cbb-bluemix"
#     };

#     const authenticator = new IamAuthenticator({ apikey: secret.IAM_API_KEY })
#     const cloudant = CloudantV1.newInstance({
#       authenticator: authenticator
#     });
#     cloudant.setServiceUrl(secret.COUCH_URL);
    
#     let dbListPromise;
#     if(params.dealerId){
#         dbListPromise = getMatchingRecords(cloudant, "dealerships", {"id":parseInt(params.dealerId)});
#     }
#     else if (params.state){
#         dbListPromise = getMatchingRecords(cloudant, "dealerships", {"state":{"$eq":params.state}});
#     }
#     else{
#         dbListPromise = getAllRecords(cloudant, "dealerships");
#     }
#     return dbListPromise;
# }


 
#  /*
#  Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
#  eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
#  */
#  function getMatchingRecords(cloudant,dbname, selector) {
#      return new Promise((resolve, reject) => {
#          cloudant.postFind({db:dbname,selector:selector})
#                  .then((result)=>{
#                    resolve({result:result.result.docs});
#                  })
#                  .catch(err => {
#                     console.log(err);
#                      reject({ err: err });
#                  });
#           })
#  }
 
                        
#  /*
#  Sample implementation to get all the records in a db.
#  */
#  function getAllRecords(cloudant,dbname) {
#      return new Promise((resolve, reject) => {
#          cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
#              .then((result)=>{
#                resolve({result:result.result.rows});
#              })
#              .catch(err => {
#                 console.log(err);
#                 reject({ err: err });
#              });
#          })
#  }
