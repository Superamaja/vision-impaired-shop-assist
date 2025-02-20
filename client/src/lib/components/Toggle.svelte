<script lang="ts">
    let { checked = $bindable(), label }: Props = $props();

    interface Props {
        checked: boolean;
        label: string;
    }
</script>

<label class="flex items-center gap-2 cursor-pointer">
    <div class="relative">
        <input type="checkbox" class="sr-only" bind:checked />
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
