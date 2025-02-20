<script lang="ts">
    let {
        value = $bindable(),
        min = 0,
        max = 100,
        label,
        step = 1,
    }: Props = $props();

    interface Props {
        value: number;
        min?: number;
        max?: number;
        label: string;
        step?: number;
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
        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
    />
</div>
