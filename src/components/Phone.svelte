<script>
    import StatusBar from "./StatusBar.svelte";
</script>

<div class="relative w-[400px] h-[765px]">
    <img
        src="/phone_border.png"
        class="w-full absolute scale-105 pointer-events-none"
        alt=""
    />
    <div class="bg-gray-800 w-full h-full rounded-3xl px-4 py-1">
        <StatusBar />
        <div class="grid grid-cols-5 border-b border-b-gray-500 pb-2">
            <div></div>
            <div class="col-span-3">
                <h1 class="text-center text-md font-bold">User 2</h1>
                <h2 class="text-center text-xs text-blue-400">Online</h2>
            </div>
            <div></div>
        </div>
    </div>
</div>
