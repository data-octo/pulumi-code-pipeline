# Pulumi Implementation for AWS CodeCommit, CodeDeploy, and CodePipeline

In this repository, we use CodePipeline to deploy code maintained in a CodeCommit repository to a single Amazon EC2 instance. The pipeline is triggered when we push a change to the CodeCommit repository. The pipeline deploys the changes to an Amazon EC2 instance using CodeDeploy as the deployment service.

The pipeline has two stages:
1. A source stage (Source) for your CodeCommit source action.
2. A deployment stage (Deploy) for your CodeDeploy deployment action.

![picture 7](images/b4337496b64e78ab2b3dbe6d4dbf71b7ee221bddf223cded16cb2f357f790168.png)  


### Step 1: Create a CodeCommit repository
![picture 1](images/70fc4e47e603c04ad6d024eca4fae6de5b4b47f9530ed88989a4b587f7ae5d5c.png)  

### Step 2: Add code to your CodeCommit repository
![picture 3](images/3b6e9582eb488975c19d2eea7484e304813734c6e095f77f7e2d3f54fb6959ef.png)  

### Step 3: Create an Amazon EC2 Linux instance and install the CodeDeploy agent
![picture 4](images/1844fae453d9d8eb9f110ecb8598953a6145728450c639408141ed862383c85e.png)  

### Step 4: Create CodeDeploy application and deployment group
![picture 5](images/f5db500a787ad392bfe299fc9389ce5a3ff5d8a2eaafab28fe97b6c0632c818b.png)  

### Step 5: Create CodePipeline with CodeCommit and CodeDeploy
![picture 6](images/22407be34375c7022a7f1ab402d769e1e48c30ed4405340e18d8e6d5aba8defc.png)  


## Reference
- https://docs.aws.amazon.com/codepipeline/latest/userguide/tutorials-simple-codecommit.html