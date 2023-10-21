const nodeName = "listenerNode";

const component = `
<div>
  <div class="title-box listener"><i class="fas fa-assistive-listening-systems"></i>Listener node</div>
  <div class="box">
    <p>Save user entry as (List like ["last_utterance"])</p>
    <textarea df-saving_keys></textarea>
    <p>Elements list</p>
    <textarea df-elements></textarea>
    <p>Timeout</p>
    <textarea df-timeout></textarea>
  </div>
</div>
`;

const menuIcon = `<div
class="drag-drawflow"
draggable="true"
ondragstart="drag(event)"
data-node="${nodeName}">
<i class="fas fa-assistive-listening-systems"></i><span> Listen Node!</span>
<div id="description_listener" style="display: none;">
    <p>Save user entry as (List like ["last_utterance"])</p>
</div>
</div>`
;

export const initListenerNode = () => {
  const menu = document.getElementById("menu-container");
  menu.insertAdjacentHTML("beforeend", menuIcon);
  // Add event listener to show description when dropdown button is clicked
  var descriptionDiv = document.getElementById("description_listener");

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

export const addListenerNode = (editor, pos_x, pos_y) => {
  editor.addNode(
    nodeName,
    1,
    1,
    pos_x,
    pos_y,
    nodeName,
    { 
      saving_keys: "[\"last_utterance\"]",
      elements: "[]",
      timeout: "Session timeout"
    },
    component
  );
};
