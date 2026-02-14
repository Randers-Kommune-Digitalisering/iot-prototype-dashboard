// Directive: v-plain-text
// Ensures contenteditable elements accept only plain text (prevents HTML insertion)
export default {
  mounted(el) {
    el.setAttribute('contenteditable', 'true');

    const insertPlainText = (text) => {
      text = text ?? '';
      // Try the simplest approach first
      try {
        if (document.queryCommandSupported && document.queryCommandSupported('insertText')) {
          document.execCommand('insertText', false, text);
          return;
        }
      } catch (e) {
        // ignore and fallback
      }

      const sel = window.getSelection();
      if (!sel || !sel.rangeCount) return;
      const range = sel.getRangeAt(0);
      range.deleteContents();
      const node = document.createTextNode(text);
      range.insertNode(node);
      // place caret after inserted node
      range.setStartAfter(node);
      range.collapse(true);
      sel.removeAllRanges();
      sel.addRange(range);
    };

    const onPaste = (e) => {
      e.preventDefault();
      const text = (e.clipboardData || window.clipboardData).getData('text/plain') || '';
      insertPlainText(text);
    };

    const onDrop = (e) => {
      e.preventDefault();
      const text = (e.dataTransfer && e.dataTransfer.getData('text/plain')) || '';
      insertPlainText(text);
    };

    // sanitize after any input (covers IME and other input methods)
    const getCaretCharacterOffsetWithin = (element) => {
      const sel = window.getSelection();
      if (!sel || !sel.rangeCount) return 0;
      const range = sel.getRangeAt(0).cloneRange();
      const preRange = range.cloneRange();
      preRange.selectNodeContents(element);
      preRange.setEnd(range.endContainer, range.endOffset);
      return preRange.toString().length;
    };

    const setCaretPosition = (element, chars) => {
      try {
        const range = document.createRange();
        let node = element;
        let remaining = chars;

        const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null);
        let currentNode = null;
        while ((currentNode = walker.nextNode())) {
          const nodeLen = currentNode.textContent.length;
          if (remaining <= nodeLen) {
            range.setStart(currentNode, remaining);
            range.collapse(true);
            const sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
            return true;
          }
          remaining -= nodeLen;
        }

        // fallback: place caret at end
        range.selectNodeContents(element);
        range.collapse(false);
        const sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        return false;
      } catch (e) {
        return false;
      }
    };

    const onInput = () => {
      const caret = getCaretCharacterOffsetWithin(el);
      const text = el.textContent || '';
      if (el.innerHTML !== text) {
        el.innerHTML = text;
        // restore caret at approximately same character offset
        setCaretPosition(el, caret);
      }
    };

    // try to intercept beforeinput for modern browsers (extra safety)
    const onBeforeInput = (e) => {
      if (e.inputType && e.inputType.startsWith('insert')) {
        // allow plain text insertion only
        if (e.data && /</.test(e.data)) {
          // block any input containing angle bracket which might be HTML
          e.preventDefault();
          insertPlainText(e.data.replace(/[<>]/g, ''));
        }
      }
    };

    el.addEventListener('paste', onPaste);
    el.addEventListener('drop', onDrop);
    el.addEventListener('input', onInput);
    el.addEventListener('beforeinput', onBeforeInput);

    el.__plainTextHandlers = { onPaste, onDrop, onInput, onBeforeInput };
  },

  unmounted(el) {
    const h = el.__plainTextHandlers || {};
    el.removeEventListener('paste', h.onPaste);
    el.removeEventListener('drop', h.onDrop);
    el.removeEventListener('input', h.onInput);
    el.removeEventListener('beforeinput', h.onBeforeInput);
    delete el.__plainTextHandlers;
  }
};
