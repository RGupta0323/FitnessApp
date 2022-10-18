const { Stack, Duration } = require('aws-cdk-lib');
const { nodejs, NodejsFunction } = require('aws-cdk-lib/aws-lambda-nodejs');
const {lambda } = require('aws-cdk/aws-lambda'); 
// const sqs = require('aws-cdk-lib/aws-sqs');

class FitnessAppStack extends Stack {
  /**
   *
   * @param {Construct} scope
   * @param {string} id
   * @param {StackProps=} props
   */
  constructor(scope, id, props) {
    super(scope, id, props);

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'FitnessAppQueue', {
    //   visibilityTimeout: Duration.seconds(300)
    // });

    /*const register_lambda = new NodejsFunction(this, "RegisterWebPageLambda", {
      entry: "./lib/src/register_lambda.js", 
      handler: "lambda_register"
    })*/ 

    new lambda.Function(this, "RegisterWebPageLambda", {
      code: lambda.Code.fromAsset('./lib/src/'), 
      functionName: "lambda_register", 
      runtime: lambda.Runtime.NodeJS_14_X, 
      timeout: cdk.Duration.seconds(300) 
    })

  }
}

module.exports = { FitnessAppStack }
