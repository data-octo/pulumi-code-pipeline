import pulumi
import pulumi_aws as aws
import json

# Create AWS CodeDeploy
def create_codedeploy():
    codedeploy_role = aws.iam.Role("codeDeployRole", name='PulumiCodeDeployRole',
    assume_role_policy="""{
    "Version": "2012-10-17",
    "Statement": [
        {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
            "Service": "codedeploy.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
        }
    ]
    }
    """)

    codedeploy_role_attch = aws.iam.RolePolicyAttachment("codeDeployRoleAttach",
        policy_arn="arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole",
        role=codedeploy_role.name)

    codedeploy_application = aws.codedeploy.Application("codeDeployApplication", name='PulumiStackDeployApplication')

    # pulumi_codedeploy_topic = aws.sns.Topic("pulumiCodeDeployTopic")

    codedeploy_deployment_group = aws.codedeploy.DeploymentGroup("codeDeployDeploymentGroup",
        app_name=codedeploy_application.name,
        deployment_group_name="EC2DeployGroup",
        service_role_arn=codedeploy_role.arn,
        ec2_tag_sets=[aws.codedeploy.DeploymentGroupEc2TagSetArgs(
            ec2_tag_filters=[
                aws.codedeploy.DeploymentGroupEc2TagSetEc2TagFilterArgs(
                    key="Project",
                    type="KEY_AND_VALUE",
                    value="preventive-security-control",
                ),
                aws.codedeploy.DeploymentGroupEc2TagSetEc2TagFilterArgs(
                    key="Owner",
                    type="KEY_AND_VALUE",
                    value="pulumi",
                ),
            ],
        )],
        # trigger_configurations=[aws.codedeploy.DeploymentGroupTriggerConfigurationArgs(
        #     trigger_events=["DeploymentFailure"],
        #     trigger_name="pulumi-codedeploy-trigger",
        #     trigger_target_arn=pulumi_codedeploy_topic.arn,
        # )],
        auto_rollback_configuration=aws.codedeploy.DeploymentGroupAutoRollbackConfigurationArgs(
            enabled=True,
            events=["DEPLOYMENT_FAILURE"],
        ),
        alarm_configuration=aws.codedeploy.DeploymentGroupAlarmConfigurationArgs(
            alarms=["pulumi-alarm-codedeploy"],
            enabled=True,
        ))