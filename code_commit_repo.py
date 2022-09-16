import pulumi
import pulumi_aws as aws

def create_repo():
# Create Pulumi IaC CodeCommit Repo
    pulumi_stack_repo = aws.codecommit.Repository("pulumi-stack-repo",
        description="Pulumi Stack and Policy Pack Repository",
        repository_name="PulumiStackRepository")

    pulumi.export('repo_ssh_url', pulumi_stack_repo.clone_url_ssh)

# # Create Pulumi Policy Pack CodeCommit Repo
# pulumi_policy_pack_repo = aws.codecommit.Repository("pulumi-policy-pack-repo",
#     description="Pulumi Policy Pack Repository",
#     repository_name="PulumiPolicyPackRepository")

# pulumi.export('pulumi_policy_pack_ssh_url', pulumi_policy_pack_repo.clone_url_ssh)

# # Create Pulumi Resources Stack CodeCommit Repo
# pulumi_stack_repo = aws.codecommit.Repository("pulumi-stack-repo",
#     description="Pulumi Stack Repository",
#     repository_name="PulumiStackRepository")

# pulumi.export('pulumi_stack_ssh_url', pulumi_stack_repo.clone_url_ssh)

# Create IAM user with ssh key
def create_iam_ssh():
    iam_user = aws.iam.User("pulumiUser", path="/")
    user_ssh_key = aws.iam.SshKey("pulumiUserSshKey",
        username=iam_user.name,
        encoding="SSH",
        public_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD3F6tyPEFEzV0LX3X8BsXdMsQz1x2cEikKDEY0aIj41qgxMCP/iteneqXSIFZBp5vizPvaoIR3Um9xK7PGoW8giupGn+EPuxIA4cDM4vzOqOkiMPhz5XK0whEjkVzTo4+S0puvDZuwIsdiW9mxhJc7tgBNL0cYlWSYVkz4G/fslNfRPW5mYAM49f4fhtxPb5ok4Q2Lg9dPKVHO/Bgeu5woMc7RY0p1ej6D4CKFE6lymSDJpW0YHX/wqE9+cfEauh7xZcG0q9t2ta6F6fmX0agvpFyZo8aFbXeUBr7osSCJNgvavWbM/06niWrOvYX2xwWdhXmXSrbX8ZbabVohBK41 mytest@mydomain.com")