### **Prompt for Agent 3 (Facets Spec Enhancer)**  

#### **Objective:**  
Your task is to **modify `variables.tf`, `outputs.tf`, and Terraform resource configurations** to conform with the `facets.yaml` specification. You will:  
✅ Ensure all **inputs match `facets.yaml` (`spec` or `inputs`)**  
✅ **Remove old outputs** and replace them with **Facets output format**  
✅ **Rewire all references** in `main.tf` and other Terraform files to align with Facets  

---

### **Automation Steps:**  

1. **Read `facets.yaml` and Extract Required Changes**  
   - Identify all **developer-facing inputs** (`spec`)  
   - Identify all **dependency-based inputs** (`inputs`)  
   - Identify **outputs** and their expected Facets format  

2. **Modify `variables.tf`**  
   - Ensure all `spec` fields exist as **Terraform variables** in `variables.tf`  
   - Ensure all `inputs` (dependency-based values) are **referenced correctly**  
   - Remove any unnecessary variables that are not part of `facets.yaml`  

   **Example: Old `variables.tf`**
   ```hcl
   variable "cluster_name" {
     description = "ECS Cluster Name"
     type        = string
   }
   ```

   **Updated for Facets (`cluster_name` moved to `spec`)**
   ```hcl
   variable "instance" {
     description = "Facets instance specification"
     type = object({
       kind    = string
       flavor  = string
       version = string
       spec    = object({
         cluster_name = string
       })
     })
   }
   ```

3. **Modify `main.tf` to Use `instance.spec` Instead of Old Variables**  
   - Replace old references like `var.cluster_name` with `var.instance.spec.cluster_name`  
   - Modify module dependencies to use `var.inputs.<input_name>`  

   **Example Before:**
   ```hcl
   resource "aws_ecs_cluster" "this" {
     name = var.cluster_name
   }
   ```

   **After Facets Update:**
   ```hcl
   resource "aws_ecs_cluster" "this" {
     name = var.instance.spec.cluster_name
   }
   ```

4. **Modify `outputs.tf` to Conform with Facets Outputs**  
   - **Remove all old-style Terraform outputs**  
   - Define Facets `output_interfaces` and `output_attributes`  

   **Example: Old `outputs.tf`**
   ```hcl
   output "cluster_id" {
     value = aws_ecs_cluster.this.id
   }
   ```

   **Updated for Facets (`output_attributes` format)**
   ```hcl
   locals {
     output_interfaces = {}
     output_attributes = {
       cluster_id = aws_ecs_cluster.this.id
     }
   }
   ```

5. **Ensure Inputs Are Correctly Wired to Terraform Resources**  
   - If an input is **dependency-based**, reference it using `var.inputs.<input_name>`  
   - If an input is **developer-provided**, use `var.instance.spec.<input_name>`  

   **Example: Handling Inputs from Another Module**  
   ```hcl
   variable "inputs" {
     type = map(any)
   }

   resource "aws_security_group" "this" {
     vpc_id = var.inputs.aws_vpc_details.vpc_id
   }
   ```

---

### **Final Handoff:**  
- ✅ Ensure `variables.tf`, `outputs.tf`, and Terraform resource references **match `facets.yaml`**  
- ✅ Remove **old Terraform outputs** and replace them with **Facets output format**  
- ✅ Verify **Terraform references (`var.instance.spec` and `var.inputs`) are correct**  
- ✅ Hand over to the **next agent** for testing and validation  

---

### **Key Transformations in Terraform Code**  
✔ Convert **developer inputs** to `var.instance.spec.<field>`  
✔ Convert **dependencies** to `var.inputs.<dependency_name>`  
✔ Replace **Terraform outputs** with `output_interfaces` & `output_attributes`  

This ensures **full Facets compatibility** with minimal developer intervention. 🚀