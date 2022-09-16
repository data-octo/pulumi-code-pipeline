
import pulumi_aws as aws
import json
# Create AWS EC2 for CodeDeploy
def create_ec2_instance():

    ec2_name = 'pulumi_ec2_codedeploy'
    ec2_type = 't2.micro'

    sg = aws.ec2.SecurityGroup(
                'ec2-codedeploy-sg',
                description="Allow HTTP traffic to EC2 instance",
                ingress=[{
                        "protocol": "tcp",
                        "from_port": 80,
                        "to_port": 80,
                        "cidr_blocks": ["0.0.0.0/0"],
                    },
                {
                    "protocol": "tcp",
                    "from_port": 443,
                    "to_port": 443,
                    "cidr_blocks": ["0.0.0.0/0"],
                },
                {
                    "protocol": "tcp",
                    "from_port": 22,
                    "to_port": 22,
                    "cidr_blocks": ["0.0.0.0/0"],
                }
                ],
            egress=[
                {
                    "protocol": "-1",
                    "from_port": 0,
                    "to_port": 0,
                    "cidr_blocks": ["0.0.0.0/0"],

                }
            ],        
        )

    #create IAM Role for SSM
    ec2_role = aws.iam.Role("pulumi-ec2-role", name="pulumi-ec2-role",
        assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                    "Service": "ec2.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
                ]
        }),
        tags={
            "Name": "pulumi-ec2-role",
        })

    instance_profile = aws.iam.InstanceProfile("pulumi-ec2-instance-profile", name="pulumi-ec2-role", role=ec2_role.name)

    ec2_role_policy_attachment = aws.iam.RolePolicyAttachment("pulumi-ec2-role-policy-ssm",
        role=ec2_role.id,
        policy_arn="arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
    )

    ec2_role_policy_attachment = aws.iam.RolePolicyAttachment("pulumi-ec2-role-policy-codedeploy",
        role=ec2_role.id,
        policy_arn="arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforAWSCodeDeploy"        
    )

    ec2_instance = aws.ec2.Instance(
            ec2_name,
            instance_type=ec2_type,
            vpc_security_group_ids=[sg.id],            
            ami='ami-0c2ab3b8efb09f272', # amazon linux ami
            iam_instance_profile=instance_profile,        
            associate_public_ip_address=True,
            tags={
                "Name":  ec2_name,
                "Project": 'preventive-security-control',
                'Owner': 'pulumi'
            },
    )
