<script lang="ts">
  /**
   * Slider Component Props Interface
   *
   * @interface Props
   * @property {number} value - Current slider value (bindable)
   * @property {number} min - Minimum allowed value (default: 0)
   * @property {number} max - Maximum allowed value (default: 100)
   * @property {string} label - Display label for the slider
   * @property {number} step - Step increment for value changes (default: 1)
   * @property {() => void} update - Optional callback fired when dragging ends
   */
  interface Props {
    value: number;
    min?: number;
    max?: number;
    label: string;
    step?: number;
    update?: () => void;
  }

  let {
    value = $bindable(),
    min = 0,
    max = 100,
    label,
    step = 1,
    update = () => {},
  }: Props = $props();
</script>

<!--
  Slider Component
  
  A customizable range slider with real-time value display and callback support.
  Optimized for touch and mouse interactions with proper accessibility labeling.
  
  Features:
  - Bindable value for two-way data binding
  - Configurable min/max/step values
  - Real-time value display in label
  - Update callback triggered only on interaction end (not during dragging)
  - Touch and mouse event support
-->
<div class="flex flex-col gap-2">
  <label class="text-sm font-medium text-gray-700" for={label}>
    {label}: {value}
  </label>
  <input
    type="range"
    {min}
    {max}
    {step}
    bind:value
    onmouseup={() => update()}
    ontouchend={() => update()}
    class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
  />
</div>
