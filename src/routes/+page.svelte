<script>
    let c1 = -0.125,
        c2 = 0.234,
        y1 = 0.492,
        y2 = -0.133;
    let key = "asdvgbjmjhmhjmgh";
    let plainText = "";
    let keyResults = [];
    let y = [0, 0];
    $: console.log(c1);
    let c1Prime, c2Prime;
    let keyError = false,
        plainTextError = false;
    let y1Prime = 0.242,
        y2Prime = -0.955;
    let cipherText = "";
    // Define the function f(x)
    function f(x) {
        return (x % 2) - 1;
    }

    function yEquation(x, c1_, c2_, y1_, y2_) {
        return f(x + c1_ * y1_ + c2_ * y2_);
    }

    function encrypt() {
        keyResults = [];
        cipherText = "";
        if (key.length < 16) {
            keyError = true;
            return;
        }
        if (plainText.length < 1) {
            plainTextError = true;
            return;
        }
        plainTextError = false;
        keyError = false;

        y[0] = y1;
        y[1] = y2;
        for (let i = 0; i < key.length; i++) {
            //console.log(y[0] + ", " + y[1]);
            let y_n = yEquation(key.charCodeAt(i), c1, c2, y[0], y[1]);
            keyResults = [...keyResults, y_n];
            y[0] = y[1];
            y[1] = y_n;
        }
        c1Prime = keyResults[14];
        c2Prime = keyResults[15];

        y[0] = y1Prime;
        y[1] = y2Prime;
        for (let i = 0; i < plainText.length; i++) {
            //console.log(y[0] + ", " + y[1]);
            let y_n = plainText.charCodeAt(i) + c1Prime * y[0] + c2Prime * y[1];

            y[0] = y[1];
            y[1] = y_n;
            let boundedCharCode = y_n % 128; // Restrict to ASCII range 0-127

            let encodedChar = String.fromCharCode(boundedCharCode);
            cipherText += encodedChar;
        }
    }
</script>

<div class="w-full min-h-[100vh] bg-gray-900">
    <main
        class="p-1 md:p-4 container m-auto grid xl:grid-cols-3 lg:grid-cols-2 grid-cols-1 md:grid-cols-2 place-items-center h-full gap-4"
    >
        <div class="grid gap-4 w-full">
            <form
                action=""
                class="bg-gray-800 text-white rounded-lg p-4 w-full grid gap-4"
            >
                <div class="flex gap-4 items-center">
                    <h3 class="font-bold">C1:</h3>
                    <input
                        bind:value={c1}
                        type="number"
                        step="0.001"
                        class="w-full bg-gray-700 rounded-md px-2 py-1"
                    />
                </div>
                <div class="flex gap-4 items-center">
                    <h3 class="font-bold">C2:</h3>
                    <input
                        bind:value={c2}
                        type="number"
                        step="0.001"
                        class="w-full bg-gray-700 rounded-md px-2 py-1"
                    />
                </div>
                <div class="flex gap-4 items-center">
                    <h3 class="font-bold">Y(-1):</h3>
                    <input
                        bind:value={y1}
                        type="number"
                        step="0.001"
                        class="w-full bg-gray-700 rounded-md px-2 py-1"
                    />
                </div>
                <div class="flex gap-4 items-center">
                    <h3 class="font-bold">Y(-2):</h3>
                    <input
                        bind:value={y2}
                        type="number"
                        step="0.001"
                        class="w-full bg-gray-700 rounded-md px-2 py-1"
                    />
                </div>
                <div class="flex gap-4 items-center">
                    <h3 class="font-bold">Y(-1)':</h3>
                    <input
                        bind:value={y1Prime}
                        type="number"
                        step="0.001"
                        class="w-full bg-gray-700 rounded-md px-2 py-1"
                    />
                </div>
                <div class="flex gap-4 items-center">
                    <h3 class="font-bold">Y(-2)':</h3>
                    <input
                        bind:value={y2Prime}
                        type="number"
                        step="0.001"
                        class="w-full bg-gray-700 rounded-md px-2 py-1"
                    />
                </div>
            </form>
            <form
                action=""
                class="bg-gray-800 text-white rounded-lg p-4 w-full grid gap-4"
            >
                <div>
                    <h3 class="font-bold">Key Input (16 Characters):</h3>
                    <input
                        maxlength="16"
                        bind:value={key}
                        type="text"
                        class="w-full mt-2 bg-gray-700 rounded-md px-2 py-1"
                    />
                    {#if keyError}
                        <h3 class="text-red-500">
                            Key Must be 16 characters long
                        </h3>
                    {/if}
                </div>
                <div>
                    <h3 class="font-bold">Plain Text</h3>
                    <input
                        bind:value={plainText}
                        type="text"
                        class="w-full mt-2 bg-gray-700 rounded-md px-2 py-1"
                    />
                    {#if plainTextError}
                        <h3 class="text-red-500">
                            Plain Text must not be empty
                        </h3>
                    {/if}
                </div>
                <button
                    on:click={encrypt}
                    class="px-2 py-1 bg-green-500 rounded-md font-bold"
                >
                    Encrypt
                </button>
            </form>
        </div>
        <section class="w-full p-1">
            <h1 class="font-bold text-lg text-white">Key System</h1>
            {#each Array(keyResults.length) as _, i}
                {#if i == 14}
                    <h4 class="text-white font-bold">
                        Index: 14; c1' = {c1Prime}
                    </h4>
                {:else if i == 15}
                    <h4 class="text-white font-bold">
                        Index: 15; c2' = {c2Prime}
                    </h4>
                {:else}
                    <h4 class="text-white">
                        <span class="font-bold">Index: {i};</span>
                        {keyResults[i]}
                    </h4>
                {/if}
            {/each}
        </section>
        <section class="w-full p-1">
            <h1 class="font-bold text-lg text-white">Main Algorithm</h1>
            <h2 class="text-white">
                <span class="font-bold">CipherText</span>
                : {cipherText}
            </h2>
        </section>
    </main>
</div>
