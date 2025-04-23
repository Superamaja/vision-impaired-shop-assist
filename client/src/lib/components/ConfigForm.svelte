<script lang="ts">
  import { onMount } from "svelte";
  import { config, fetchConfig, updateConfig } from "../stores/states.svelte";
  import Slider from "./Slider.svelte";
  import Toggle from "./Toggle.svelte";
  import TextInput from "./TextInput.svelte";

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

  <TextInput
    label="TTS OCR Template"
    bind:value={config.TTS_OCR_TEMPLATE}
    update={updateConfig}
    placeholder={"{text}"}
  />
  <p class="text-xs text-gray-500 mt-1">
    Available variables: <code>{"{text}"}</code>
  </p>

  <TextInput
    label="TTS Barcode Found Template"
    bind:value={config.TTS_BARCODE_FOUND_TEMPLATE}
    update={updateConfig}
    placeholder={"Product: {product_name}, Brand: {brand}"}
  />
  <p class="text-xs text-gray-500 mt-1">
    Available variables: <code>{"{product_name}"}</code>,
    <code>{"{brand}"}</code>, <code>{"{allergies}"}</code>
  </p>

  <TextInput
    label="TTS Barcode Not Found Template"
    bind:value={config.TTS_BARCODE_NOT_FOUND_TEMPLATE}
    update={updateConfig}
    placeholder={"Unknown barcode scanned"}
  />
  <p class="text-xs text-gray-500 mt-1">
    Available variables: <code>{"{barcode}"}</code>
  </p>
</form>
