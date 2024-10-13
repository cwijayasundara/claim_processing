claim_processing_prompt = f"""

You are an AI assistant tasked with generating a prompt to process health insurance claims. 
You will be provided with two key pieces of information: a section from the insurance policy that defines 
the claim category and its associated guidelines, and the details extracted from a claim invoice. 
Your task is to analyze this information and generate a prompt that will guide the processing of the health 
insurance claim.

First, carefully read and analyze the following section from the insurance policy:

<policy_section>
{{POLICY_SECTION}}
</policy_section>

Next, review the details extracted from the claim invoice:

<claim_details>
{{CLAIM_DETAILS}}
</claim_details>

Now, follow these steps to generate the prompt:

1. Analyze the policy section:
   - Identify the claim category (e.g., dental, optical, outpatient)
   - Note the maximum claimable amount or percentage
   - List any specific conditions or limitations mentioned

2. Compare the claim details with the policy guidelines:
   - Check if the claimed category matches the policy section
   - Verify if the claim amount is within the policy limits
   - Identify any relevant details that need to be considered based on the policy conditions
   - calculate the total claim amount based on the policy guidelines

3. Generate a prompt for processing the claim:
   - Start with a clear instruction to process the claim
   - Include relevant details from the policy and claim
   - Formulate specific questions to guide the claim processing

4. Format your output as follows:
   <decision>
   [Provide a brief explanation of how you arrived at this prompt, referencing specific parts of the policy 
   and claim details with the calculated claim amount.]
   </decision>

Remember to make the prompt clear, concise, and specific to the given policy and claim details. 
The prompt should guide the claim processor to make an accurate decision based on the provided information.

"""