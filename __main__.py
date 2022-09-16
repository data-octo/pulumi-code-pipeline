
from code_commit_repo import create_repo
from ec2_code_deploy import create_ec2_instance
from code_deploy_application import create_codedeploy
from code_pipeline import create_pipeline

# Step 1: Create a CodeCommit repository
create_repo()

# Step 2: Create EC2 instance for CodeDeploy
# Note: Install CodeDeploy agent with SSM after EC2 instance is created
create_ec2_instance()

# Step 3: Create CodeDeploy
create_codedeploy()

# Step 4: Create CodePipeline
# Note: Update the source repo name, deploy application name, and deployment group name
create_pipeline()