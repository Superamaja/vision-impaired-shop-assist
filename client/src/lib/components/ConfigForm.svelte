<script lang="ts">
    import { onMount } from "svelte";
    import { config, fetchConfig, updateConfig } from "../stores/states.svelte";
    import Slider from "./Slider.svelte";
    import Toggle from "./Toggle.svelte";

    onMount(() => {
        fetchConfig();
    });
</script>

<form class="space-y-6 max-w-md mx-auto p-4">
    <Toggle
        label="Debug Mode"
        bind:checked={config.DEBUG}
        update={updateConfig}
    />

    <Slider
        label="Text-to-Speech Speed"
        min={100}
        max={500}
        bind:value={config.TTS_SPEED}
        update={updateConfig}
    />

    <Slider
        label="Image Thresholding"
        min={0}
        max={255}
        bind:value={config.THRESHOLDING}
        update={updateConfig}
    />
</form>
