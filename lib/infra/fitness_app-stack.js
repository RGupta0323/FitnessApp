const { Stack, Duration } = require('aws-cdk-lib');
const { NodejsFunction } = require('aws-cdk-lib/aws-lambda-nodejs');
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

    const register_lambda = new nodejs.NodejsFunction(this, "RegisterWebPageLambda",{
      entry: "./lib/src/register_lambda.js", 
      handler: "lambda_register"
    } )
  }
}

module.exports = { FitnessAppStack }
