const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {
        secret ={
        "COUCH_URL": "https://ec96a461-e711-4471-8075-8e077c690cbb-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY":"jUh8BbgAAd-qRBUBCHe0iHc6vxF6jKMK4pzEiqTQgCpF",
        "COUCH_USERNAME":"ec96a461-e711-4471-8075-8e077c690cbb-bluemix"
    };

    const authenticator = new IamAuthenticator({ apikey: secret.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(secret.COUCH_URL);
    
    let dbListPromise;
    if(params.dealerId){
        dbListPromise = getMatchingRecords(cloudant, "dealerships", {"id":parseInt(params.dealerId)});
    }
    else if (params.state){
        dbListPromise = getMatchingRecords(cloudant, "dealerships", {"state":{"$eq":params.state}});
    }
    else{
        dbListPromise = getAllRecords(cloudant, "dealerships");
    }
    return dbListPromise;
}


 
 /*
 Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
 eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
 */
 function getMatchingRecords(cloudant,dbname, selector) {
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:dbname,selector:selector})
                 .then((result)=>{
                   resolve({result:result.result.docs});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
 }
 
                        
 /*
 Sample implementation to get all the records in a db.
 */
 function getAllRecords(cloudant,dbname) {
     return new Promise((resolve, reject) => {
         cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
             .then((result)=>{
               resolve({result:result.result.rows});
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
 }






// from ibmcloudant.cloudant_v1 import CloudantV1
// from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


// # main() will be run automatically when this action is invoked in IBM Cloud
// def main(dict):
//     """
//     Gets the car reviews for a specified dealership
//     :param dict: Cloud Functions actions accept a single parameter, which must be a JSON object.
//                 In this case, the param must be an a JSON object with the key "dealerId" with the dealership id as value (string or int)
//                 I.e: {"dealerId": "15"}
//     :return: The action returns a JSON object consisting of the HTTP response with all reviews for the given dealership.
//     """

//     secret = {
//         "URL":  "https://ec96a461-e711-4471-8075-8e077c690cbb-bluemix.cloudantnosqldb.appdomain.cloud",
//         "IAM_API_KEY": "jUh8BbgAAd-qRBUBCHe0iHc6vxF6jKMK4pzEiqTQgCpF",
//         "ACCOUNT_NAME":  "ec96a461-e711-4471-8075-8e077c690cbb-bluemix",
//     }
//     authenticator = IAMAuthenticator(secret["IAM_API_KEY"])
//     service = CloudantV1(authenticator=authenticator)
//     service.set_service_url(secret['URL'])
    

    
//     response = service.post_document(
//                 db='reviews',
//                 document=dict["review"]).get_result()
//     try: 
//         # result_by_filter=my_database.get_query_result(selector,raw_result=True) 
//         result= {
//             'headers': {'Content-Type':'application/json'}, 
//             'body': {'data':response} 
//             }        
//         return result
//     except:  
//         return { 
//             'statusCode': 404, 
//             'message': 'Something went wrong'
//             }

