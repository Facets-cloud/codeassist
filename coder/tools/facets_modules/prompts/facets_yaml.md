### **Refined Prompt for Facets YAML Agent**

#### **Objective:**

Your task is to **autonomously generate `facets.yaml`** for a given Terraform module, and hand over the module
path to the Agent 3 (Facets Refactor Agent). 

This file should accurately
define:  
✅ **Intent & Flavor (lowercase, hyphen-separated)**  
✅ **Cloud provider support**  
✅ **Inputs (`spec` for developer configuration vs. `inputs` for dependencies)**  
✅ **Outputs & provider handling**  
✅ **Dependency management**

---

### **Automation Steps:**

1. **Extract Metadata from the Terraform Module:**
    - Receive **path to module** from Agent 1.
    - Determine:
        - **Intent** → What capability the module provides (e.g., `aws-ecs-cluster`).
        - **Flavor** → Specific implementation (e.g., `spot-instance`).
        - **Cloud provider(s)** → Extract from `main.tf`.

2. **Construct `facets.yaml` Autonomously:**
    - Populate `intent`, `flavor`, `version`, `clouds`.
    - Identify **developer-facing inputs (`spec`)** from `variables.tf`.
    - Identify **dependency inputs (`inputs`)** from `variables.tf` and existing Facets output types.
    - Identify **outputs** (`@output/<output_type>`).

3. **Handle Provider Consumption & Exposure:**
    - If the module **declares a provider**, it **must come from an input** (not hardcoded).  
      **Example:** If `provider "google"` is detected →
      ```yaml
      inputs:
        gcp_auth:
          type: "@output/gcp-auth"
          providers:
            - google
      ```
    - If the module **outputs a provider**, confirm with the user before exposing it as a Facets output.  
      **Example:**
      ```yaml
      outputs:
        default:
          type: "@output/kubernetes_cluster_details"
          providers:
            helm:
              source: hashicorp/helm
              version: 2.8.0
              attributes:
                kubernetes:
                  host: attributes.endpoint
                  cluster_ca_certificate: attributes.ca_certificate
                  token: attributes.client_token
      ```

4. **Differentiate Inputs (`spec` vs. `inputs` from dependencies):**
    - **`spec` (developer-defined inputs)** → Configurable resource options (e.g., instance size, enable/disable flags).
    - **`inputs` (dependencies from other modules)** → Operational infrastructure (e.g., VPC, IAM roles, network IDs).
    - **Ask user when unsure:**
      > "Should `<input_name>` come from another module (dependency) or be specified by the developer?"  
      _(IAM roles, networking, shared services typically come from dependencies.)_

---

### **Refined `facets.yaml` Examples Based on Uploaded Files**

#### ✅ **Example 1: AWS ECS Service (`ecs_service`)**

```yaml
intent: ecs-service
flavor: rohit-ecs-service
clouds:
  - aws

version: 1.0

spec:
  image:
    type: string
    description: "The Docker image to use for the ECS service."

inputs:
  ecs_cluster_details:
    type: "@output/ecs_cluster_details"
  aws_vpc_details:
    type: "@output/aws_vpc_details"

outputs:
  default:
    type: "@output/ecs_service_details"

sample:
  kind: ecs-service
  flavor: rohit-ecs-service
  version: "1.0"
  spec:
    image: "nginx:latest"
```

---

#### ✅ **Example 2: AWS ECS Cluster (`ecs_cluster`)**

```yaml
intent: ecs-cluster
flavor: rohit-ecs-cluster
clouds:
  - aws

version: 1.0

spec: { }

outputs:
  default:
    type: "@output/ecs_cluster_details"

sample:
  kind: ecs-cluster
  flavor: rohit-ecs-cluster
  version: "1.0"
  spec: { }
```

---

#### ✅ **Example 3: AWS Public VMs (`aws-public-vms`)**

```yaml
intent: misc
flavor: aws-public-vms
version: 1.0
clouds:
  - aws

spec:
  instance_count:
    type: integer
    description: "Number of VMs to create"
  region:
    type: string
    enum: [ "us-east-1", "us-west-1", "us-west-2", "ap-south-1", "us-east-2" ]
    description: "AWS region to deploy the VMs"
  instance_type:
    type: string
    enum: [ "t3.micro", "t3.small", "t3.medium", "t3.large", "t3.xlarge" ]

outputs:
  default:
    type: "@output/aws_vm_details"
    providers:
      - aws

sample:
  kind: "misc"
  flavor: "aws-public-vms"
  version: "1.0"
  spec:
    instance_count: 2
    region: "us-east-1"
```

---

### **Final Handoff:**

- ✅ Validate `facets.yaml` structure.
- ✅ Save in module directory.
- ✅ Pass module path to **Agent 3 (Facets Spec Enhancer)** for further refinements.

---

### **Why These Refinements?**

✔ **Matches Facets conventions:** Intent & flavor are **lowercase, hyphen-separated**.  
✔ **Automates provider handling:** Modules **consume** providers via `inputs`, **expose** providers via `outputs`.  
✔ **Smart input classification:** Ops-specific inputs **come from dependencies**, while developer-configurable
options **go in spec**.

This ensures **Facets YAML Agent is fully autonomous**, while still confirming critical dependencies with the user. 🚀