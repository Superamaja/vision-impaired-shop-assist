<script lang="ts">
  import { onMount } from "svelte";

  type Barcode = {
    barcode: string;
    product_name: string;
    brand: string;
  };

  let barcodes: Barcode[] = $state([]);
  let newBarcode = $state({ barcode: "", product_name: "", brand: "" });
  let error = $state("");
  let success = $state("");

  async function fetchBarcodes() {
    try {
      const response = await fetch("http://localhost:5001/api/barcodes");
      barcodes = await response.json();
    } catch (e) {
      error = "Failed to fetch barcodes";
    }
  }

  async function addBarcode(event: Event) {
    event.preventDefault();
    try {
      const response = await fetch("http://localhost:5001/api/barcodes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newBarcode),
      });
      if (response.ok) {
        await fetchBarcodes();
        newBarcode = { barcode: "", product_name: "", brand: "" };
        success = "Barcode added successfully";
        setTimeout(() => (success = ""), 5000);
      } else {
        const data = await response.json();
        error = data.error || "Failed to add barcode";
      }
    } catch (e) {
      error = "Failed to add barcode";
    }
  }

  async function deleteBarcode(barcode: string) {
    try {
      const response = await fetch(
        `http://localhost:5001/api/barcodes/${barcode}`,
        {
          method: "DELETE",
        },
      );
      if (response.ok) {
        await fetchBarcodes();
        success = "Barcode deleted successfully";
        setTimeout(() => (success = ""), 5000);
      } else {
        error = "Failed to delete barcode";
      }
    } catch (e) {
      error = "Failed to delete barcode";
    }
  }

  onMount(fetchBarcodes);
</script>

<div class="space-y-6 max-w-6xl mx-auto p-4">
  <h2 class="text-2xl font-bold mb-4">Barcode Management</h2>

  {#if error}
    <div
      class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4"
    >
      {error}
    </div>
  {/if}

  {#if success}
    <div
      class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4"
    >
      {success}
    </div>
  {/if}

  <form
    onsubmit={addBarcode}
    class="space-y-4 bg-white p-6 rounded-lg shadow-sm"
  >
    <div>
      <label for="product_name" class="block text-sm font-medium text-gray-700"
        >Product Name</label
      >
      <input
        id="product_name"
        type="text"
        bind:value={newBarcode.product_name}
        required
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
      />
    </div>
    <div>
      <label for="brand" class="block text-sm font-medium text-gray-700"
        >Brand</label
      >
      <input
        id="brand"
        type="text"
        bind:value={newBarcode.brand}
        required
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
      />
    </div>
    <div>
      <label for="barcode" class="block text-sm font-medium text-gray-700"
        >Barcode</label
      >
      <input
        id="barcode"
        type="text"
        bind:value={newBarcode.barcode}
        required
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
      />
    </div>
    <button
      type="submit"
      class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
    >
      Add Barcode
    </button>
  </form>

  <div class="mt-8">
    <h3 class="text-xl font-semibold mb-4">Saved Barcodes</h3>

    {#if barcodes.length === 0}
      <p class="text-gray-500 text-center py-6">
        No barcodes found. Add one above.
      </p>
    {:else}
      <div
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4"
      >
        {#each barcodes as barcode}
          <div class="bg-white shadow-sm rounded-lg p-4 flex flex-col h-full">
            <div class="flex-grow">
              <p class="font-medium text-lg">
                {barcode.product_name}
              </p>
              <p class="text-sm text-gray-600">
                Barcode: {barcode.barcode}
              </p>
              <p class="text-sm text-gray-600 mb-3">
                Brand: {barcode.brand}
              </p>
            </div>
            <div class="mt-auto pt-2 border-t">
              <button
                onclick={() => deleteBarcode(barcode.barcode)}
                class="text-red-600 hover:text-red-800 focus:outline-none text-sm"
              >
                Delete
              </button>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>
