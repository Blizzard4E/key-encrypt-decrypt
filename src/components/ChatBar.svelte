<script>
    import { PUBLIC_FLASK_API } from "$env/static/public";
    import { onMount } from "svelte";

    export let phone, owner, otherOwner;

    let inputText;
    let isSending = false;

    function addTextChat() {
        if (inputText == "" || isSending) return;
        isSending = true;
        fetch(`${PUBLIC_FLASK_API}/text`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json", // Set Content-Type to application/json
            },
            body: JSON.stringify({
                original_text: inputText,
                key: phone.key,
            }),
        })
            .then((res) => res.json())
            .then((data) => {
                console.log(data);
                phone.chats = [
                    ...phone.chats,
                    {
                        owner: owner,
                        encrypted: data.encrypted_text,
                        decrypted: data.decrypted_text,
                    },
                ];
                inputText = "";
                isSending = false;
            });

        let chatListOwner = document.getElementById(owner);
        let chatListOtherOwner = document.getElementById(otherOwner);
        setTimeout(() => {
            chatListOwner.scrollTop = chatListOwner.scrollHeight;
            chatListOtherOwner.scrollTop = chatListOtherOwner.scrollHeight;
        }, 50);
    }
</script>

<ul
    class="flex items-center gap-2 px-4 pt-2 border-t border-t-gray-600"
    class:brightness-50={isSending}
    class:pointer-events-none={isSending}
>
    <li>
        <img src="/image.png" class="w-6" alt="" />
    </li>
    <li>
        <img src="/video.png" class="w-6" alt="" />
    </li>
    <li>
        <img src="/mic.png" class="w-6" alt="" />
    </li>
    <li>
        <input
            bind:value={inputText}
            on:keydown={(events) => {
                if (events.key == "Enter") {
                    addTextChat();
                }
            }}
            type="text"
            placeholder="Text..."
            class="w-52 bg-gray-700 rounded-full px-3 py-1 focus:outline-none"
        />
    </li>
    <button on:click={addTextChat}>
        <img src="/send.png" class="w-6" alt="" />
    </button>
</ul>
