const { Stack, Duration, cdk} = require('aws-cdk-lib');
const { Construct } = require("constructs");
const apigateway = require("aws-cdk-lib/aws-apigateway");
const lambda = require("aws-cdk-lib/aws-lambda");
const s3 = require("aws-cdk-lib/aws-s3");
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
      runtime: lambda.Runtime.NodeJS_14_X
    })

  }
}

module.exports = { FitnessAppStack }
