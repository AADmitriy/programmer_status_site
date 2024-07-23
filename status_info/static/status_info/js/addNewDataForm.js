function addForm(formListId, emptyFormId, formPrefix, managementPrefix, formClass='data_input') {
    const totalForms = document.getElementById(`id_${managementPrefix}-TOTAL_FORMS`);
    const formList = document.getElementById(formListId);
    const currentForms = formList.getElementsByClassName(formClass);
    const copyFormTarget = document.getElementById(formListId);
    const emptyFormCopy = document.getElementById(emptyFormId).cloneNode(true);
    emptyFormCopy.setAttribute("class", formClass);
    emptyFormCopy.setAttribute("id", `${formPrefix}_form_${currentForms.length}`);
    const emptyFormCopyInputs = emptyFormCopy.getElementsByTagName("input");
    for (let inputEl of emptyFormCopyInputs) {
        if (inputEl.type != 'text' && inputEl.type != 'number') {
            continue;
        }
        inputEl.required = true;
    }
    emptyFormCopyTextAreas = emptyFormCopy.getElementsByTagName("textarea");
    for (let TextArea of emptyFormCopyTextAreas) {
        TextArea.required = true;
    }
    const regex = new RegExp('__prefix__', 'g');
    emptyFormCopy.innerHTML = emptyFormCopy.innerHTML.replace(regex, currentForms.length);
    totalForms.setAttribute("value", currentForms.length + 1);
    copyFormTarget.append(emptyFormCopy);
}

function removeForm(closeButton, formListId, managementPrefix, formClass='data_input') {
    const formDiv = closeButton.closest(`div.${formClass}`);
    var sibs = [];
    var elem = formDiv.nextSibling;
    while (elem != null) {
        if (elem.nodeType === 3) continue;
        sibs.push(elem);
        elem = elem.nextSibling;
    }

    sibs.forEach((sib) => {
        var regex = /\d+/;
        var number = sib.id.match(regex)[0];
        const new_number = number - 1;
        sib.id = sib.id.replace(regex, new_number);
        var select_values = [];
        var input_values = [];
        var textarea_values = [];
        for (let input of sib.getElementsByTagName("select")) {
            select_values.push(input.value);
        }
        for (let input of sib.getElementsByTagName("input")) {
            if (input.type == 'checkbox') {
                input_values.push(input.checked)
            }
            else {
                input_values.push(input.value);
            }
        }
        for (let input of sib.getElementsByTagName("textarea")) {
            textarea_values.push(input.value);
        }
        var regex_inner = /-\d+-/g;
        sib.innerHTML = sib.innerHTML.replace(regex_inner, `-${new_number}-`);
        for (let input of sib.getElementsByTagName("select")) {
            input.value = select_values.shift();
        }
        for (let input of sib.getElementsByTagName("input")) {
            if (input.type == 'checkbox') {
                input.checked = input_values.shift();
            }
            else {
                input.value = input_values.shift();
            }
        }
        for (let input of sib.getElementsByTagName("textarea")) {
            input.value = textarea_values.shift();
        }
    });

    formDiv.remove();
    const formList = document.getElementById(formListId);
    const currentForms = formList.getElementsByClassName(formClass);
    if (currentForms.length == 0) {
        const errorList = document.getElementById(`${managementPrefix}_error_list`);
        errorList.innerHTML = "";
    }
    const totalForms = document.getElementById(`id_${managementPrefix}-TOTAL_FORMS`);
    totalForms.setAttribute("value", currentForms.length);
}

function pasteCounterHtml(element) {
    const wrapperHtml = document.createElement("div");
    wrapperHtml.className = "textarea_wrapper";
    element.parentNode.insertBefore(wrapperHtml, element);
    wrapperHtml.appendChild(element);
    counterHtml = '<div class="the-count"><span class="current">0</span><span class="maximum"> / ' + element.maxLength +
    '</span></div>';
    element.insertAdjacentHTML("afterend", counterHtml);
    element.setAttribute("onkeyup", "processTextareaCounterOnkeyup(this)")
}

function processTextareaCounter(event) {
    const wrapper = event.target.closest('.textarea_wrapper');
    var current = wrapper.querySelector('span.current');
    current.textContent = event.target.value.length;
}

function processTextareaCounterOnkeyup(element) {
    const wrapper = element.closest('.textarea_wrapper');
    var current = wrapper.querySelector('span.current');
    current.textContent = element.value.length;
}

function processCounter(event) {
    const wrapper = event.target.closest('.textarea_wrapper');
    var current = wrapper.querySelector('span.current');
    current.textContent = event.target.value.length;
}

function setUpCounter(element) {
    element.setAttribute("onkeyup", "processTextareaCounterOnkeyup(this)")
    const wrapper = element.closest('.textarea_wrapper');
    var maximum = wrapper.querySelector('span.maximum');
    maximum.textContent = ` / ${element.maxLength}`;
}