<script lang="ts">
  /**
   * Toggle Component Props Interface
   *
   * @interface Props
   * @property {boolean} checked - Current toggle state (bindable)
   * @property {string} label - Display label for the toggle
   * @property {() => void} update - Optional callback fired on state change
   */
  interface Props {
    checked: boolean;
    label: string;
    update?: () => void;
  }

  let { checked = $bindable(), label, update = () => {} }: Props = $props();
</script>

<!--
  Toggle Component
  
  A custom toggle switch component with smooth animations and accessibility features.
  Provides a modern alternative to traditional checkboxes with visual feedback.
  
  Features:
  - Bindable checked state for two-way data binding
  - Smooth CSS transitions for state changes
  - Screen reader accessible with proper labeling
  - Callback support for handling state changes
-->
<label class="flex items-center gap-2 cursor-pointer">
  <div class="relative">
    <input
      type="checkbox"
      class="sr-only"
      bind:checked
      onchange={() => update()}
    />
    <div
      class={`block w-14 h-8 rounded-full transition-colors ${
        checked ? "bg-blue-600" : "bg-gray-300"
      }`}
    ></div>
    <div
      class={`absolute left-1 top-1 bg-white w-6 h-6 rounded-full transition-transform ${
        checked ? "translate-x-6" : "translate-x-0"
      }`}
    ></div>
    <span class="text-sm font-medium text-gray-700">{label}</span>
  </div>
</label>
