// PromptWizard Console Tests

async function runTests() {
    console.log('Starting PromptWizard Console Tests');

    let testCategory1, testCategory2, testPrompt1, testPrompt2;

    try {
        // Test 1: Create a new category
        console.log('Test 1: Creating a new category');
        const categoryResponse = await axios.post(`${API_URL}/categories`, { name: 'Test Category 1' });
        testCategory1 = categoryResponse.data;
        console.log('Test Category 1 created:', testCategory1);

        // Test 2: Create a prompt and assign it to the category
        console.log('Test 2: Creating a prompt in Test Category 1');
        const promptResponse1 = await axios.post(`${API_URL}/prompts`, {
            name: 'Test Prompt 1',
            contents: 'This is a test prompt',
            category_id: testCategory1.id
        });
        testPrompt1 = promptResponse1.data;
        console.log('Test Prompt 1 created:', testPrompt1);

        // Test 3: Create a new category and prompt simultaneously
        console.log('Test 3: Creating a new category and prompt simultaneously');
        const newCategoryResponse = await axios.post(`${API_URL}/categories`, { name: 'Test Category 2' });
        testCategory2 = newCategoryResponse.data;
        console.log('Test Category 2 created:', testCategory2);

        const promptResponse2 = await axios.post(`${API_URL}/prompts`, {
            name: 'Test Prompt 2',
            contents: 'This is another test prompt',
            category_id: testCategory2.id
        });
        testPrompt2 = promptResponse2.data;
        console.log('Test Prompt 2 created:', testPrompt2);

        // Test 4: Move a prompt to a different category
        console.log('Test 4: Moving Test Prompt 2 to Test Category 1');
        await axios.put(`${API_URL}/prompts/${testPrompt2.id}`, {
            name: testPrompt2.name,
            contents: testPrompt2.contents,
            category_id: testCategory1.id
        });
        console.log('Test Prompt 2 moved to Test Category 1');

        // Verify prompt movement
        const promptsAfterMove = await axios.get(`${API_URL}/prompts?category_id=${testCategory1.id}`);
        console.log('Prompts in Test Category 1 after move:', promptsAfterMove.data);

        // Test 5: Delete Test Prompt 2
        console.log('Test 5: Deleting Test Prompt 2');
        await axios.delete(`${API_URL}/prompts/${testPrompt2.id}`);
        console.log('Test Prompt 2 deleted');

        // Verify prompt deletion
        const promptsAfterDeletion = await axios.get(`${API_URL}/prompts?category_id=${testCategory1.id}`);
        console.log('Prompts after deletion:', promptsAfterDeletion.data);

        // Test 6: Delete Test Category 1 with Test Prompt 1 still in it
        console.log('Test 6: Deleting Test Category 1 with Test Prompt 1 still in it');
        await axios.delete(`${API_URL}/categories/${testCategory1.id}`);
        console.log('Test Category 1 deleted');

        // Verify category deletion
        const categoriesAfterDeletion = await axios.get(`${API_URL}/categories`);
        console.log('Categories after deletion:', categoriesAfterDeletion.data);

        // Test 7: Attempt to delete the already deleted category (Test Category 1)
        console.log('Test 7: Attempting to delete the already deleted Test Category 1');
        try {
            await axios.delete(`${API_URL}/categories/${testCategory1.id}`);
        } catch (error) {
            if (error.response && error.response.status === 404) {
                console.log('Expected 404 error received when trying to delete already deleted category');
            } else {
                throw error;
            }
        }

        // Test 8: Delete the remaining category (Test Category 2)
        console.log('Test 8: Deleting Test Category 2');
        await axios.delete(`${API_URL}/categories/${testCategory2.id}`);
        console.log('Test Category 2 deleted');

        // Verify final state
        const finalCategories = await axios.get(`${API_URL}/categories`);
        console.log('Final categories:', finalCategories.data);

        const finalPrompts = await axios.get(`${API_URL}/prompts`);
        console.log('Final prompts:', finalPrompts.data);

        console.log('All tests completed successfully');
    } catch (error) {
        console.error('Test failed:', error.message);
        console.error('Error details:', error.response?.data);
    }
}