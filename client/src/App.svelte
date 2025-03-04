<script lang="ts">
    import ConfigForm from "./lib/components/ConfigForm.svelte";
    import BarcodeManager from "./lib/components/BarcodeManager.svelte";
</script>

<main class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto py-12">
        <h1 class="text-3xl font-bold text-center text-gray-900 mb-8">
            Vision Assistant Settings
        </h1>
        <div class="space-y-12">
            <ConfigForm />
            <BarcodeManager />
        </div>
    </div>
</main>
