const nodeName = "ifNode";
const icon = '<i class="fas fa-map-signs"></i>';
const tittleClass = "if";
const tittle = "Conditional";

const component = `
<div>
  <div class="title-box ${tittleClass}">${icon}${tittle}</div>
  <div class="box">
    <p>Variable</p>
    <input type="text" df-variable>
    <p>Condition</p>
    <select df-condition>
        <option value="equals">equals</option>
        <option value="greater_than">greater than</option>
        <option value="less_than">less than</option>
        <option value="not_equals">not equals</option>
        <option value="contains">contains</option>
        <option value="not_contains">not contains</option>
    </select>
    <p>Type</p>
    <select df-type>
        <option value="text">text</option>
        <option value="number">number</option>
        <option value="boolean">boolean (true/false)</option>
    </select>
    <p>Value</p>
    <input type="text" df-value>
    </div>
</div>
`;


const menuIcon = `<div
class="drag-drawflow"
draggable="true"
ondragstart="drag(event)"
data-node="${nodeName}">
${icon}<span> ${tittle}</span>
<div id="description_${nodeName}" style="display: none;">
    <p>Checks if variable meets a condition...!</p>
</div>
</div>`
;

export const initIfNode = () => {
  const menu = document.getElementById("menu-container");
  menu.insertAdjacentHTML("beforeend", menuIcon);
  // Add event listener to show description when dropdown button is clicked
  var descriptionDiv = document.getElementById(`description_${nodeName}`);

    // Get a reference to the element you want to click on
    var element = document.querySelector(`div.drag-drawflow[data-node="${nodeName}"]`);

    // Add a click event listener to the element
    element.addEventListener("click", function () {
        // Toggle the display of the description div
        if (descriptionDiv.style.display === "none") {
            descriptionDiv.style.display = "block";
        } else {
            descriptionDiv.style.display = "none";
        }
    });
};

export const addIfNode = (editor, pos_x, pos_y) => {
  editor.addNode(
    nodeName,
    1,
    1,
    pos_x,
    pos_y,
    nodeName,
    { 
        variable: "[\"last_utterance\"]",
        condition: "equals",
        type: "text",
        value: "value"
    },
    component
  );
};
