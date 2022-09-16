import pulumi
import pulumi_aws as aws
import json


# Create AWS CodePipeline for CodeCommit and CodeDeploy
def create_pipeline():

    source_repository_name = "PulumiStackRepository"
    codedeploy_application_name = "PulumiStackDeployApplication"
    deployment_group_name = "EC2DeployGroup"

    codepipeline_bucket = aws.s3.Bucket("pulumiCodepipelineBucket", 
        acl="private",
        tags={            
            "Name": "pulumiCodepipelineBucket",
        })

    codepipeline_bucket_policy = """
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicRead",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": "arn:aws:s3:::pulumicodepipelinebucket-fb32351/*"
            }
        ]
    }
    """

    codepipeline_role = aws.iam.Role("codepipelineRole", name="PulumiCodePipelineRole",
        assume_role_policy="""{
            "Version": "2012-10-17",
            "Statement": [
                {
                "Effect": "Allow",
                "Principal": {
                    "Service": "codepipeline.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
                }
            ]
            }
            """)

    codepipeline_role_attach = aws.iam.RolePolicyAttachment("awsAdminAccess",
        policy_arn="arn:aws:iam::aws:policy/AdministratorAccess",
        role=codepipeline_role.name)


    # s3kmskey = aws.kms.get_alias(name="alias/pulumi-kms-key")

    # s3kmskey = aws.kms.Key("pulumi-key",
    #     deletion_window_in_days=10,
    #     description="Pulumi KMS key")

    codepipeline = aws.codepipeline.Pipeline("codepipeline", name="PulumiStackPipeline",
            
        # artifact_stores=[aws.codepipeline.PipelineArtifactStoreArgs(
        #     location=codepipeline_bucket.bucket,
        #     type="S3",
        #     encryption_key=aws.codepipeline.PipelineArtifactStoreEncryptionKeyArgs(
        #         id=s3kmskey.arn,
        #         type="KMS",
        #     ),
        # )],

        artifact_store=aws.codepipeline.PipelineArtifactStoreArgs(
                    location=codepipeline_bucket.bucket,
                    type="S3",
                    # encryption_key=aws.codepipeline.PipelineArtifactStoreEncryptionKeyArgs(
                    #     id=s3kmskey.arn,
                    #     type="KMS",
                    # ),
                ),
        
        role_arn=codepipeline_role.arn,
        
        stages=[
            
            aws.codepipeline.PipelineStageArgs(
                name="Source",
                actions=[
                    aws.codepipeline.PipelineStageActionArgs(
                        name="Source",
                        category="Source",
                        owner="AWS",
                        provider="CodeCommit",
                        version="1",
                        output_artifacts=["source_output"],
                        
                        configuration={
                            "RepositoryName": source_repository_name,
                            "BranchName": "master",
                            "OutputArtifactFormat": "CODE_ZIP"
                        },
                    )
                ],
            ),  

            aws.codepipeline.PipelineStageArgs(
                name="Deploy",
                actions=[aws.codepipeline.PipelineStageActionArgs(
                    name="Deploy",
                    category="Deploy",
                    owner="AWS",
                    provider="CodeDeploy",
                    input_artifacts=["source_output"],
                    version="1",
                    configuration={
                        "ApplicationName":codedeploy_application_name,
                        "DeploymentGroupName": deployment_group_name
                    },
                )],
            ),
        ])

