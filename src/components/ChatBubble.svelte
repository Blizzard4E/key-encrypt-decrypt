<script>
    import { onMount } from "svelte";

    export let phone, owner, index;
    let isOwner;
    let hasLastMessage;
    let hasNewMessage;
    let isLastMessage;

    $: if (phone.chats[index].owner == owner) {
        isOwner = true;
    } else {
        isOwner = false;
    }
    $: if (index > 0) {
        if (phone.chats[index].owner == phone.chats[index - 1].owner) {
            hasLastMessage = true;
        }
    }
    $: if (index < phone.chats.length - 1) {
        if (phone.chats[index].owner == phone.chats[index + 1].owner) {
            hasNewMessage = true;
            isLastMessage = false;
        } else {
            isLastMessage = true;
        }
    } else {
        isLastMessage = true;
    }
</script>

<div
    class="flex transition-all items-center px-3 py-[2px]"
    class:justify-end={owner == phone.chats[index].owner}
    class:mt-auto={index == 0}
    class:pb-2={index == phone.chats.length - 1}
>
    {#if isOwner}
        <div
            class="p-1 px-4 bg-green-500 rounded-3xl"
            class:rounded-tr-lg={hasLastMessage}
            class:rounded-br-lg={hasNewMessage && !isLastMessage}
            class:rounded-br-none={isLastMessage}
        >
            {#if phone.encryptMode}
                {phone.chats[index].encrypted}
            {:else}
                {phone.chats[index].decrypted}
            {/if}
        </div>
    {:else}
        <div
            class="p-1 px-4 bg-gray-700 rounded-3xl"
            class:rounded-tl-lg={hasLastMessage}
            class:rounded-bl-lg={hasNewMessage && !isLastMessage}
            class:rounded-bl-none={isLastMessage}
        >
            {#if phone.encryptMode}
                {phone.chats[index].encrypted}
            {:else}
                {phone.chats[index].decrypted}
            {/if}
        </div>
    {/if}
</div>
