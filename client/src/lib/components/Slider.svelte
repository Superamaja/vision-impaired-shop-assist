<script lang="ts">
  let {
    value = $bindable(),
    min = 0,
    max = 100,
    label,
    step = 1,
    update = () => {},
  }: Props = $props();

  interface Props {
    value: number;
    min?: number;
    max?: number;
    label: string;
    step?: number;
    update?: () => void;
  }
</script>

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
