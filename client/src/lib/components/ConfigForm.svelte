<script lang="ts">
    import { onMount } from "svelte";
    import { config, fetchConfig, updateConfig } from "../stores/states.svelte";
    import Slider from "./Slider.svelte";
    import Toggle from "./Toggle.svelte";

    onMount(() => {
        fetchConfig();
    });

    const handleSubmit = (event: Event) => {
        event.preventDefault();
        updateConfig();
    };
</script>

<form class="space-y-6 max-w-md mx-auto p-4">
    <Toggle label="Debug Mode" bind:checked={config.DEBUG} />

    <Slider
        label="Text-to-Speech Speed"
        min={100}
        max={500}
        bind:value={config.TTS_SPEED}
    />

    <Slider
        label="Image Thresholding"
        min={0}
        max={255}
        bind:value={config.THRESHOLDING}
    />

    <button
        type="submit"
        class="bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600"
        on:click={handleSubmit}
    >
        Submit
    </button>
</form>
